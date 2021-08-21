"""
Module for requesting to URL and get page's html code from there,
download media files, check that the request if correct, page in RNC exists.
"""

__all__ = (
    'get_htmls', 'is_request_correct', 'download_docs'
)

import asyncio
import logging
import time
from typing import List, Tuple

import aiofiles
import aiohttp
import bs4

logger = logging.getLogger("rnc")
WAIT = 24


class BaseRequestError(Exception):
    pass


class NoResultFound(BaseRequestError):
    pass


class LastPageDoesntExist(BaseRequestError):
    pass


class WrongHTTPRequest(BaseRequestError):
    pass


async def fetch_html(url: str,
                     ses: aiohttp.ClientSession,
                     **kwargs) -> Tuple[int, str] or None:
    """ Coro, obtaining page's HTML code.

    This coro should be awaited from a worker.

    :return: tuple of int and str, page index and its HTML code.
     None if there's an error, -1 if it's 429 and the worker should
     wait some time and make request again.

    :exception: all exceptions should be processed here.
    """
    worker_name = kwargs.pop('worker_name', '')
    try:
        resp = await ses.get(url, params=kwargs)
    except Exception as e:
        logger.error(
            f"{e}\n{worker_name}Cannot get "
            f"answer from '{url}' with {kwargs}")
        return

    if resp.status == 200:
        text = await resp.text('utf-8')
        resp.close()
        return kwargs['p'], text
    elif resp.status == 429:
        resp.close()
        return -1

    logger.error(
        f"{worker_name}{resp.status} -- '{resp.reason}' "
        f"requesting to {resp.url}"
    )
    resp.close()


async def worker_fetching_html(worker_name: str,
                               q_args: asyncio.Queue,
                               q_results: asyncio.Queue) -> None:
    """
    Worker requesting to URL with args from
     q_args and putting results to q_results.

    Wait some time and request again if there's 429 error.
    """
    while True:
        url, ses, kwargs = q_args.get_nowait()
        logger.debug(
            f"{worker_name}Requested to '{url}' with '{kwargs}'")

        res = await fetch_html(url, ses, **kwargs, worker_name=worker_name)

        if res is None:
            q_args.task_done()
            return

        while res == -1:
            logger.debug(
                    f"{worker_name}429 'Too many requests', "
                    f"page: {kwargs['p']}; wait {WAIT}s"
            )

            await asyncio.sleep(WAIT)
            res = await fetch_html(url, ses, **kwargs, worker_name=worker_name)

        logger.debug(
            f"{worker_name}Received from '{url}' with '{kwargs}'")
        q_args.task_done()

        await q_results.put((res[0], res[1]))


async def get_htmls_coro(url: str,
                         start: int,
                         stop: int,
                         **kwargs) -> List[str]:
    """
    Coro running 5 workers doing requests and
     getting HTML codes of the pages.

    URLs will be created for i in range(start, stop),
    HTTP tag 'p' (page) is i.

    """
    timeout = aiohttp.ClientTimeout(WAIT)

    q_results = asyncio.Queue(maxsize=-1)
    q_args = asyncio.Queue(maxsize=-1)

    async with aiohttp.ClientSession(timeout=timeout) as ses:
        for p_index in range(start, stop):
            await q_args.put((url, ses, {**kwargs, 'p': p_index}))

        tasks = []
        for worker_index in range(5):
            name = f"Worker-{worker_index + 1}: "
            task = asyncio.create_task(
                worker_fetching_html(name, q_args, q_results)
            )
            tasks += [task]

        await q_args.join()

        for task in tasks:
            task.cancel()

        results = [
            q_results.get_nowait()
            for _ in range(q_results.qsize())
        ]
    results.sort(key=lambda res: res[0])
    return [
        html for _, html in results
    ]


def get_htmls(url: str,
              start: int = 0,
              stop: int = 1,
              **kwargs) -> List[str]:
    """ Run coro, get html codes of the pages."""
    logger.info(f"Requested to '{url}' [{start};{stop}) with params {kwargs}")
    coro_start = time.time()

    html_codes = asyncio.run(
        get_htmls_coro(url, start, stop, **kwargs)
    )

    logger.info("Request was successfully completed")
    logger.info(f"Coro executing time: {round(time.time() - coro_start, 2)}")
    return html_codes


async def get_htmls_async(url: str,
                          start: int = 0,
                          stop: int = 1,
                          **kwargs) -> List[str]:
    """ Run coro, get html codes of the pages."""
    logger.info(f"Requested to '{url}' [{start};{stop}) with params {kwargs}")
    coro_start = time.time()

    html_codes = await get_htmls_coro(url, start, stop, **kwargs)

    logger.info("Request was successfully completed")
    logger.info(f"Coro executing time: {round(time.time() - coro_start, 2)}")
    return html_codes


def whether_result_found(url: str,
                         **kwargs) -> str:
    """
    Whether the page contains results.

    :return: first page HTML code if everything is OK.

    :exception RuntimeError: if HTTP request was wrong.
    :exception ValueError: if the result not found.
    """
    logger.debug("Validating that the request is OK")
    try:
        page_html = get_htmls(url, **kwargs)[0]
    except Exception:
        logger.error(f"The request is not correct: {kwargs}")
        raise RuntimeError
    logger.debug("The request is correct")

    logger.debug("Validating that the result exits")
    soup = bs4.BeautifulSoup(page_html, 'lxml')

    # TODO: сузить круг поиска
    content = soup.find('div', {'class': 'content'}).text
    res_msg = ('По этому запросу ничего не найдено.' in content or
               'No results match the search query.' in content)
    if res_msg:
        raise ValueError
    return page_html


def does_page_exist(url: str,
                    p_index: int,
                    first_page: str,
                    **kwargs) -> str:
    """
    Whether a page at the index exists.

    It means, the number of the page in 'pager' is equal to expected index.
    RNC redirects to the first page if the page at the number doesn't exist.
    Here it's assumed, that the request's correct.

    :return: last page code if everything is OK.

    :exception ValueError: the page doesn't exist.
    """
    # indexing starts with 0
    start = p_index
    start = start * (start >= 0)
    stop = p_index + 1

    # request's correct → first page exists
    if stop == 1:
        return first_page

    last_page = get_htmls(url, start, stop, **kwargs)[0]
    soup = bs4.BeautifulSoup(last_page, 'lxml')

    pager = soup.find('p', {'class': 'pager'})
    if pager:
        max_page_number = max(
            int(page.text)
            for page in pager.find_all('a')
            if page.text.isdigit()
        )
        if not max_page_number:
            raise ValueError
        if max_page_number < stop:
            raise ValueError
        return last_page

    # if there's no pager, but result exists.
    # this might happen if expand=full or out=kwic
    if last_page == first_page:
        raise ValueError
    return last_page


def is_request_correct(url: str,
                       p_count: int,
                       **kwargs) -> Tuple[str, str]:
    """
    Check:
        – is the HTTP request correct (means there are no exceptions catch).

        – has there been any result.

        – does a page at the number exist (
        means RNC doesn't redirect to the first page).

    :return: first and last pages if everything's OK.

    :exception WrongHTTPRequest: HTTP request is wrong.
    :exception NoResultFound: no result found.
    :exception LastPageDoesntExist: the last page doesn't exist.
    """
    logger.debug("Validating that everything is OK")
    try:
        # to reduce the number of requests
        # the two checks are combined into one.
        # coro writes logs by itself
        first_page = whether_result_found(url, **kwargs)
    except ValueError:
        logger.error("HTTP request is OK, but no result found")
        raise NoResultFound(f"{kwargs}")
    except RuntimeError:
        logger.error("HTTP request is wrong")
        raise WrongHTTPRequest(f"{kwargs}")
    logger.debug("HTTP request is correct, result found")

    logger.debug("Validating that the last page exists")
    try:
        last_page = does_page_exist(url, p_count - 1, first_page, **kwargs)
    except ValueError:
        logger.error("Everything is OK, but last page doesn't exist")
        raise LastPageDoesntExist(f"{kwargs}")
    logger.debug("The last page exists")

    logger.debug("Validated successfully")
    return first_page, last_page


async def whether_result_found_async(url: str,
                                     **kwargs) -> str:
    """
    Whether the page contains results.

    :return: first page HTML code if everything is OK.

    :exception RuntimeError: if HTTP request was wrong.
    :exception ValueError: if the result not found.
    """
    logger.debug("Validating that the request is OK")
    try:
        page_html = (await get_htmls_async(url, **kwargs))[0]
    except Exception:
        logger.error(f"The request is not correct: {kwargs}")
        raise RuntimeError
    logger.debug("The request is correct")

    logger.debug("Validating that the result exits")
    soup = bs4.BeautifulSoup(page_html, 'lxml')

    # TODO: сузить круг поиска
    content = soup.find('div', {'class': 'content'}).text
    res_msg = ('По этому запросу ничего не найдено.' in content or
               'No results match the search query.' in content)
    if res_msg:
        raise ValueError
    return page_html


async def does_page_exist_async(url: str,
                                p_index: int,
                                first_page: str,
                                **kwargs) -> str:
    """
    Whether a page at the index exists.

    It means, the number of the page in 'pager' is equal to expected index.
    RNC redirects to the first page if the page at the number doesn't exist.
    Here it's assumed, that the request's correct.

    :return: last page code if everything is OK.

    :exception ValueError: the page doesn't exist.
    """
    # indexing starts with 0
    start = p_index
    start = start * (start >= 0)
    stop = p_index + 1

    # request's correct → first page exists
    if stop == 1:
        return first_page

    last_page = (await get_htmls_async(url, start, stop, **kwargs))[0]
    soup = bs4.BeautifulSoup(last_page, 'lxml')

    pager = soup.find('p', {'class': 'pager'})
    if pager:
        max_page_number = max(
            int(page.text)
            for page in pager.find_all('a')
            if page.text.isdigit()
        )
        if not max_page_number:
            raise ValueError
        if max_page_number < stop:
            raise ValueError
        return last_page

    # if there's no pager, but result exists.
    # this might happen if expand=full or out=kwic
    if last_page == first_page:
        raise ValueError
    return last_page


async def is_request_correct_async(url: str,
                                   p_count: int,
                                   **kwargs) -> Tuple[str, str]:
    """
    Check:
        – is the HTTP request correct (means there are no exceptions catch).

        – has there been any result.

        – does a page at the number exist (
        means RNC doesn't redirect to the first page).

    :return: first and last pages if everything's OK.

    :exception WrongHTTPRequest: HTTP request is wrong.
    :exception NoResultFound: no result found.
    :exception LastPageDoesntExist: the last page doesn't exist.
    """
    logger.debug("Validating that everything is OK")
    try:
        # to reduce the number of requests
        # the two checks are combined into one.
        # coro writes logs by itself
        first_page = await whether_result_found_async(url, **kwargs)
    except ValueError:
        logger.error("HTTP request is OK, but no result found")
        raise NoResultFound(f"{kwargs}")
    except RuntimeError:
        logger.error("HTTP request is wrong")
        raise WrongHTTPRequest(f"{kwargs}")
    logger.debug("HTTP request is correct, result found")

    logger.debug("Validating that the last page exists")
    try:
        last_page = await does_page_exist_async(url, p_count - 1, first_page, **kwargs)
    except ValueError:
        logger.error("Everything is OK, but last page doesn't exist")
        raise LastPageDoesntExist(f"{kwargs}")
    logger.debug("The last page exists")

    logger.debug("Validated successfully")
    return first_page, last_page


async def fetch_media_file(url: str,
                           ses: aiohttp.ClientSession,
                           **kwargs) -> bytes or int:
    """
    Coro, getting media content to write.

    :return: bytes (media) if everything is OK,
     -1 if there's 429 error, None if it is another error.

    :exception: all exceptions should be processed here.
    """
    worker_name = kwargs.pop('worker_name', '')
    try:
        resp = await ses.get(url, allow_redirects=True, params=kwargs)
    except Exception as e:
        logger.error(
            f"{e}\n{worker_name}Cannot get "
            f"answer from '{url}' with {kwargs}")
        return

    if resp.status == 200:
        content = await resp.read()
        resp.close()
        return content
    elif resp.status == 429:
        resp.close()
        return -1

    logger.error(
        f"{resp.status}: {resp.reason} requesting to {resp.url}"
    )
    resp.close()


async def dump(content: bytes,
               filename: str) -> None:
    """ Dump content to media file."""
    async with aiofiles.open(filename, 'wb') as f:
        await f.write(content)


async def worker_fetching_media(worker_name: str,
                                q_args: asyncio.Queue) -> None:
    """
    Worker getting media file and dumping it to file.

    Wait some time and request again if there's 429 error.
    """
    while True:
        url, ses, filename = q_args.get_nowait()

        logger.debug(f"{worker_name}Requested to '{url}'")
        content = await fetch_media_file(url, ses, worker_name=worker_name)

        if content is None:
            q_args.task_done()
            return

        while content == -1:
            logger.debug(
                f"{worker_name}: 429 'Too many requests', "
                f"url: {url}; wait {WAIT}s"
            )

            await asyncio.sleep(WAIT)
            content = await fetch_media_file(url, ses, worker_name=worker_name)

        logger.debug(f"{worker_name}Received from '{url}'")
        logger.debug(f"{worker_name}Dumping '{url}' to '{filename}'")
        await dump(content, filename)
        logger.debug(f"{worker_name}'{filename}' dumped")

        q_args.task_done()


async def download_docs_coro(url_to_name: List[Tuple[str, str]]) -> None:
    """ Coro running 5 workers to download media files. """
    timeout = aiohttp.ClientTimeout(WAIT)
    q_args = asyncio.Queue(maxsize=-1)

    async with aiohttp.ClientSession(timeout=timeout) as ses:
        for url, filename in url_to_name:
            await q_args.put((url, ses, filename))

        tasks = []
        for worker_number in range(5):
            name = f"Worker-{worker_number + 1}: "
            task = asyncio.create_task(
                worker_fetching_media(name, q_args))
            tasks += [task]

        await q_args.join()

        for task in tasks:
            task.cancel()


def download_docs(url_to_name: List[Tuple[str, str]]) -> None:
    """
    Run coro, download the files.

    :param url_to_name: list of tuples of str, pairs: url – filename.
    """
    logger.info(f"Requested {len(url_to_name)} files to download")
    coro_start = time.time()

    asyncio.run(download_docs_coro(url_to_name))

    logger.info(f"Downloading completed, coro executing time: "
                f"{round(time.time() - coro_start, 2)}s")


async def download_docs_async(url_to_name: List[Tuple[str, str]]) -> None:
    """
    Run coro, download the files.

    :param url_to_name: list of tuples of str, pairs: url – filename.
    """
    logger.info(f"Requested {len(url_to_name)} files to download")
    coro_start = time.time()

    await download_docs_coro(url_to_name)

    logger.info(f"Downloading completed, coro executing time: "
                f"{round(time.time() - coro_start, 2)}s")
