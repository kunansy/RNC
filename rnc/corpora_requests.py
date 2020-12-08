"""
Module for requesting to URL and get page's html code from there,
download media files, check that the request if correct, page in RNC exists.
"""

__all__ = 'get_htmls', 'is_request_correct'

import aiofiles
import aiohttp
import aiojobs
import asyncio
import bs4
from typing import List, Tuple

import rnc.corpora_logging as clog

logger = clog.create_logger(__name__)
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
    except Exception as e:
        logger.exception(f"Cannot get answer from RNC:\n{e}")
        return

    try:
        if resp.status != 429:
            resp.raise_for_status()
    except Exception:
        logger.error(
            f"{resp.status}: {resp.reason} requesting to {resp.url}")
        resp.close()
        return

    if resp.status == 200:
        text = await resp.text('utf-8')
        await queue.put((kwargs['p'], text))
    elif resp.status == 429:
        logger.debug(
            f"429, {resp.reason} Page: {kwargs['p']}, wait {WAIT}s")
        resp.close()
        await asyncio.sleep(WAIT)
        await fetch(url, ses, queue, **kwargs)


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
            await scheduler.spawn(fetch(url, ses, queue, **kwargs, p=p_index))

        while len(scheduler) is not 0:
            await asyncio.sleep(.5)
        await scheduler.close()

        results = [
            await queue.get()
            for _ in range(queue.qsize())
        ]
    results.sort(key=lambda res: res[0])
    return [
        html for p, html in results
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
        get_htmls_coro(url, start, stop, **kwargs))
    logger.info("Request was completed successfully")
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
                         **kwargs) -> bool:
    """ Whether the page contains results.

    :param url: str, request url.
    :param kwargs: request HTTP tags.
    :exception RuntimeError: if HTTP request was wrong.
    """
    try:
        page_html = get_htmls(url, **kwargs)[0]
    except Exception:
        raise RuntimeError

    soup = bs4.BeautifulSoup(page_html, 'lxml')

    # TODO: сузить круг поиска
    content = soup.find('div', {'class': 'content'}).text
    res_msg = ('По этому запросу ничего не найдено.' in content or
               'No results match the search query.' in content)
    return not res_msg


def does_page_exist(url: str,
                    p_index: int,
                    **kwargs) -> bool:
    """ Whether a page at the index exists.

    It means, the number of the page in 'pager' is equal to expected index.
    RNC redirects to the first page if the page at the number doesn't exist.
    Here it's assumed, that the request's correct.

    :param url: str, URL.
    :param p_index: int, index of page. Indexing starts with 0.
    :param kwargs: HTTP tags.
    :return: bool, whether a page exists.
    """
    # indexing starts with 0
    start = p_index
    start = start * (start >= 0)
    stop = p_index + 1

    # request's correct → first page exists
    if stop is 1:
        return True

    page_html = get_htmls(url, start, stop, **kwargs)[0]
    soup = bs4.BeautifulSoup(page_html, 'lxml')

    pager = soup.find('p', {'class': 'pager'})
    if pager:
        p_num = pager.b
        if not p_num:
            return False
        # page index from pager should be equal to expected index
        return p_num.text == str(stop)

    # if there's no pager, but result exists.
    # this might happen if expand=full or out=kwic
    first_page_code = get_htmls(url, 0, 1, **kwargs)[0]
    return page_html != first_page_code


def is_request_correct(url: str,
                       p_count: int,
                       **kwargs) -> bool:
    """ Check:
        – is the HTTP request correct (means there're no exceptions catch).

        – has there been any result.

        – does a page at the number exist (
        means RNC doesn't redirect to the first page).

    :param url: str, request url.
    :param p_count: int, request count of pages.
    :param kwargs: request HTTP tags.
    :return: True if everything's OK, an exception otherwise.
    :exception ValueError: something's wrong.
    """
    try:
        # to reduce the number of requests
        # the two checks are combined into one.
        # coro writes logs by itself
        assert whether_result_found(url, **kwargs) is True
    except AssertionError:
        raise ValueError("No result found")
    except RuntimeError:
        raise ValueError("Wrong HTTP request")

    if not does_page_exist(url, p_count - 1, **kwargs):
        raise ValueError("Last page doesn't exist")

    return True


async def fetch_download(url: str,
                         ses: aiohttp.ClientSession,
                         filename: str) -> str:
    """ Coro, downloading and writing media file from RNC.
    There's ClientTimeout = 25s.

    If response status == 429 sleep 24s and try again.

    :param url: str, file's url.
    :param ses: aiohttp.ClientSession.
    :param filename: str, name of the file.
    :return: str, name of the file.
    :exception: all exceptions should be processed here.
    """
    wait = 24
    timeout = aiohttp.ClientTimeout(wait + 1)
    async with ses.get(url, allow_redirects=True, timeout=timeout) as resp:
        if resp.status == 200:
            content = await resp.read()
            async with aiofiles.open(filename, 'wb') as f:
                await f.write(content)
            return filename
        elif resp.status == 429:
            await asyncio.sleep(wait)
            return await fetch_download(url, ses, filename)
        resp.raise_for_status()


async def download_docs_coro(url_to_name: List[Tuple[str, str]]) -> None:
    """ Coro executing fetch_download coro, catching exceptions.

    :param url_to_name: list of tuples of str, pairs: url – filename.
    :return None.
    """
    async with aiohttp.ClientSession() as ses:
        tasks = [
            asyncio.create_task(fetch_download(url, ses, filename))
            for url, filename in url_to_name
        ]
        while True:
            done, pending = await asyncio.wait(tasks)
            msg = "While downloading or writing file"
            for future in done:
                try:
                    filename = future.result()
                except aiohttp.ClientResponseError:
                    # 5.., 404 etc
                    logger.exception(msg)
                    raise
                except aiohttp.ClientConnectionError:
                    # there's no connection or access to the site
                    logger.exception(msg)
                    raise
                except aiohttp.InvalidURL:
                    # wrong url or params
                    logger.exception(msg)
                    raise
                except aiohttp.ServerTimeoutError:
                    # timeout
                    logger.exception(msg)
                    raise
                except Exception:
                    # another error
                    logger.exception(msg)
                    raise
                else:
                    logger.debug(f"{filename} successfully downloaded")
                    return


def download_docs(url_to_name: List[Tuple[str, str]]) -> None:
    """ Run coro, download the files.

    :param url_to_name: list of tuples of str, pairs: url – filename.
    :return: None.
    """
    logger.info(f"Requested {len(url_to_name)} files to download")
    asyncio.run(download_docs_coro(url_to_name))
    logger.info(f"Downloading successfully completed")
