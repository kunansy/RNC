"""
Module for requesting to URL and get page's html code from there,
download media files, check that the request if correct, page in RNC exists.
"""

__all__ = 'get_htmls', 'is_request_correct'

import asyncio
import logging
from typing import List, Tuple

import aiofiles
import aiohttp
import aiojobs
import bs4

logger = logging.getLogger("rnc")
WAIT = 24


async def fetch(url: str,
                ses: aiohttp.ClientSession,
                queue: asyncio.Queue,
                **kwargs) -> None:
    """ Coro, obtaining page's html code.

    If response status == 429 sleep and try again.

    :param url: str, URL to get its html code.
    :param ses: aiohttp.ClientSession.
    :param queue: asyncio.Queue, queue to where put the results:
    'p' key to sort results and html code, decoded to UTF-8.
    :param kwargs: HTTP tags.
    :return: None.
    :exception: all exceptions should be processed here.
    """
    try:
        resp = await ses.get(url, params=kwargs)
    except Exception:
        logger.exception("Cannot get answer from RNC")
        return

    if resp.status == 200:
        text = await resp.text('utf-8')
        await queue.put((kwargs['p'], text))
    elif resp.status == 429:
        logger.debug(
            f"429, {resp.reason} Page: {kwargs['p']}, wait {WAIT}s"
        )
        resp.close()
        await asyncio.sleep(WAIT)
        await fetch(url, ses, queue, **kwargs)
    else:
        logger.error(
            f"{resp.status}: {resp.reason} requesting to {resp.url}"
        )

    resp.close()


async def get_htmls_coro(url: str,
                         start: int,
                         stop: int,
                         **kwargs) -> List[str]:
    """ Coro doing requests and catching exceptions.

    URLs will be created for i in range(start, stop),
    HTTP tag 'p' (page) is i.

    :param url: str, URL.
    :param start: int, start page index.
    :param stop: int, stop page index.
    :param kwargs: HTTP tags.
    :return: list of str, html codes of the pages.
    """
    timeout = aiohttp.ClientTimeout(WAIT)
    # this limit might be wrong, it is
    # just not demanded to set any limit
    queue = asyncio.Queue(maxsize=100_000)

    async with aiohttp.ClientSession(timeout=timeout) as ses:
        scheduler = await aiojobs.create_scheduler(limit=None)
        for p_index in range(start, stop):
            try:
                await scheduler.spawn(
                    fetch(url, ses, queue, **kwargs, p=p_index)
                )
            except Exception as e:
                logger.error(f"{e} requesting to {url} with {kwargs}")

        while len(scheduler) is not 0:
            await asyncio.sleep(.5)
        await scheduler.close()

        results = [
            await queue.get()
            for _ in range(queue.qsize())
        ]
    results.sort(key=lambda res: res[0])
    return [
        html for _, html in results
    ]


def get_htmls(url: str,
              start: int = 0,
              stop: int = 1,
              **kwargs) -> List[str]:
    """ Run coro, get html codes of the pages.

    URLs will be created for i in range(start, stop),
     HTTP tag 'p' (page) is i.

    :param url: str, URL.
    :param start: int, start page index.
    :param stop: int, stop page index.
    :param kwargs: HTTP tags.
    :return: list of str, html codes of the pages.
    """
    logger.info(f"Requested: ({start};{stop}), with params {kwargs}")
    html_codes = asyncio.run(
        get_htmls_coro(url, start, stop, **kwargs)
    )
    logger.info("Request was successfully completed ")
    return html_codes


def is_http_request_correct(url: str,
                            **kwargs) -> bool:
    """ Whether the request is correct.
    It's correct If there's no exception catch.

    :param url: str, request url.
    :param kwargs: request HTTP tags.
    :return: bool, whether the request is correct.
    """
    # coro writes logs by itself
    try:
        htmls = get_htmls(url, **kwargs)
    except Exception:
        return False
    return bool(htmls)


def whether_result_found(url: str,
                         **kwargs) -> str:
    """ Whether the page contains results.

    :param url: str, request url.
    :param kwargs: request HTTP tags.
    :return: str, first page HTML code if everything is OK.

    :exception RuntimeError: if HTTP request was wrong.
    :exception ValueError: if the result not found.
    """
    logger.debug("Validating that the request is OK")
    try:
        page_html = get_htmls(url, **kwargs)[0]
    except Exception:
        logger.exception("The request is not correct")
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
    """ Whether a page at the index exists.

    It means, the number of the page in 'pager' is equal to expected index.
    RNC redirects to the first page if the page at the number doesn't exist.
    Here it's assumed, that the request's correct.

    :param url: str, URL.
    :param p_index: int, index of page. Indexing starts with 0.
    :param first_page: str, first page code.
    :param kwargs: HTTP tags.
    :return: str, last page code if everything is OK, an exception otherwise.
    """
    # indexing starts with 0
    start = p_index
    start = start * (start >= 0)
    stop = p_index + 1

    # request's correct → first page exists
    if stop is 1:
        return first_page

    last_page = get_htmls(url, start, stop, **kwargs)[0]
    soup = bs4.BeautifulSoup(last_page, 'lxml')

    pager = soup.find('p', {'class': 'pager'})
    if pager:
        p_num = pager.b
        if not p_num:
            raise ValueError
        # page index from pager should be equal to expected index
        if p_num.text != str(stop):
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
    """ Check:
        – is the HTTP request correct (means there're no exceptions catch).

        – has there been any result.

        – does a page at the number exist (
        means RNC doesn't redirect to the first page).

    :param url: str, request url.
    :param p_count: int, request count of pages.
    :param kwargs: request HTTP tags.
    :return: tuple of str, first and last pages if everything's OK,
     an exception otherwise.
    :exception ValueError: HTTP request is wrong, no result found or
     the last page doesn't exist.
    """
    logger.debug("Validating that everything is OK")
    try:
        # to reduce the number of requests
        # the two checks are combined into one.
        # coro writes logs by itself
        first_page = whether_result_found(url, **kwargs)
    except ValueError:
        logger.exception("HTTP request is OK, but no result found")
        raise ValueError("No result found")
    except RuntimeError:
        logger.exception("HTTP request is wrong")
        raise ValueError("Wrong HTTP request")
    else:
        logger.debug("HTTP request is correct, result found")

    logger.debug("Validating that the last page exists")
    try:
        last_page = does_page_exist(url, p_count - 1, first_page, **kwargs)
    except ValueError:
        logger.error("Everything is OK, but last page doesn't exist")
        raise ValueError("Last page doesn't exist")
    logger.debug("The last page exists")

    logger.debug("Validated successfully")

    return first_page, last_page


async def fetch_download(url: str,
                         ses: aiohttp.ClientSession,
                         filename: str,
                         **kwargs) -> None:
    """ Coro, downloading and writing media file from RNC.

    If response status == 429 sleep 24s and try again.

    :param url: str, file's url.
    :param ses: aiohttp.ClientSession.
    :param filename: str, name of the file.
    :param kwargs: HTTP tags to request.
    :return: None.
    :exception: all exceptions should be processed here.
    """
    try:
        resp = await ses.get(url, allow_redirects=True, params=kwargs)
    except Exception:
        logger.exception("Cannot get answer from RNC")
        return

    if resp.status == 200:
        content = await resp.read()
        async with aiofiles.open(filename, 'wb') as f:
            await f.write(content)
    elif resp.status == 429:
        logger.debug(
            f"429, {resp.reason} downloading '{filename}', wait {WAIT}s"
        )
        resp.close()
        await asyncio.sleep(WAIT)
        await fetch_download(url, ses, filename)
    else:
        logger.error(
            f"{resp.status}: {resp.reason} requesting to {resp.url}"
        )
    resp.close()


async def download_docs_coro(url_to_name: List[Tuple[str, str]]) -> None:
    """ Coro executing fetch_download coro, catching exceptions.

    :param url_to_name: list of tuples of str, pairs: url – filename.
    :return None.
    """
    timeout = aiohttp.ClientTimeout(WAIT)
    async with aiohttp.ClientSession(timeout=timeout) as ses:
        scheduler = await aiojobs.create_scheduler(limit=None)
        for url, filename in url_to_name:
            try:
                await scheduler.spawn(
                    fetch_download(url, ses, filename)
                )
            except Exception as e:
                logger.error(f"{e} requesting to {url}")

        while len(scheduler) != 0:
            await asyncio.sleep(.5)

        await scheduler.close()


def download_docs(url_to_name: List[Tuple[str, str]]) -> None:
    """ Run coro, download the files.

    :param url_to_name: list of tuples of str, pairs: url – filename.
    :return: None.
    """
    logger.info(f"Requested {len(url_to_name)} files to download")
    asyncio.run(download_docs_coro(url_to_name))
    logger.info(f"Downloading successfully completed")
