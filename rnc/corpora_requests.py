"""
Module for requesting to URL and get page's html code.

There's function checking, that:
– HTTP request is correct, means noe exception catch while requesting.
– The page exists, means results found.
– The page at the number exists, means Corpus didn't redirect to the first page,

There's ClientTimeout in the requesting function.

"""
__all__ = 'get_htmls', 'is_request_correct'

import asyncio
import logging
from typing import List, Tuple

import aiohttp
import bs4

import rnc.corpora_logging as clog

log_file = clog.log_folder / f"{__name__}.log"
formatter = clog.create_formatter()

stream_handler = clog.create_stream_handler(formatter=formatter)
file_handler = clog.create_file_handler(
    log_path=log_file, formatter=formatter)

logger = clog.create_logger(
    __name__, logging.DEBUG, file_handler, stream_handler)


async def fetch(url: str,
                ses: aiohttp.ClientSession,
                **kwargs) -> Tuple[int, str]:
    """ Coro, obtaining page's html code. There's ClientTimeout.

    If response.status == 429 sleep and try again.
    If response.status != 429 and != 200, raise an exception.

    :param url: string, URL to get its html code.
    :param ses: aiohttp.ClientSession.
    :param kwargs: HTTP tags.
    :return: p key to sort results and html code, decoded to UTF-8.
    """
    wait = 24
    t_out = aiohttp.ClientTimeout(wait + 1)
    async with ses.get(url, params=kwargs, timeout=t_out) as resp:
        if resp.status == 200:
            return kwargs['p'], await resp.text('utf-8')
        elif resp.status == 429:
            await asyncio.sleep(wait)
            return await fetch(url, ses, **kwargs)
        resp.raise_for_status()


async def get_htmls_coro(url: str,
                         p_index_start: int,
                         p_index_stop: int,
                         **kwargs) -> List[str]:
    """ Coro doing requests and catching exceptions.

    URLs will be created for i in range(p_index_start, p_index_stop),
    HTTP tag 'p' (page) is i.

    :param url: str, URL.
    :param p_index_start: int, start page index.
    :param p_index_stop: int, stop page index.
    :param kwargs: HTTP tags.
    :return: list of str, html codes of the pages.

    :exception aiohttp.ClientResponseError:
    :exception aiohttp.ClientConnectionError:
    :exception aiohttp.InvalidURL:
    :exception aiohttp.ServerTimeoutError:
    :exception Exception: another one.
    """
    async with aiohttp.ClientSession() as ses:
        tasks = [
            asyncio.create_task(fetch(url, ses, p=p_index, **kwargs))
            for p_index in range(p_index_start, p_index_stop)
        ]

        if not tasks:
            msg = "Empty range given"
            logger.error(msg)
            raise ValueError(msg)

        html_codes = []
        while True:
            done, pending = await asyncio.wait(tasks)
            for future in done:
                try:
                    page_code = future.result()
                except aiohttp.ClientResponseError:
                    # 5.., 404 etc
                    logger.exception(f"Params: {kwargs}")
                    raise
                except aiohttp.ClientConnectionError:
                    # there's no connection or access to the site
                    logger.exception(f"Params: {kwargs}")
                    raise
                except aiohttp.InvalidURL:
                    # wrong url or params
                    logger.exception(f"Params: {kwargs}")
                    raise
                except aiohttp.ServerTimeoutError:
                    # timeout
                    logger.exception(f"Params: {kwargs}")
                    raise
                except Exception:
                    # another error
                    logger.exception(f"Params: {kwargs}")
                    raise
                else:
                    html_codes += [page_code]
            # TODO: add pages' html codes as they are obtained
            # TODO: return here?
            # sort pages: 1, 2, ...
            html_codes.sort(key=lambda x: x[0])
            html_codes = [i[1] for i in html_codes]
            return html_codes


def get_htmls(url: str,
              p_index_start: int = 0,
              p_index_stop: int = 1,
              **kwargs) -> List[str]:
    """ Run coro, get html codes of the pages.

    URLs will be created for i in range(p_index_start, p_index_stop),
     HTTP tag 'p' (page) is i.

    :param url: str, URL.
    :param p_index_start: int, start page index.
    :param p_index_stop: int, stop page index.
    :param kwargs: HTTP tags.
    :return: list of str, html codes of the pages.

    :exception aiohttp.ClientResponseError:
    :exception aiohttp.ClientConnectionError:
    :exception aiohttp.InvalidURL:
    :exception aiohttp.ServerTimeoutError:
    :exception Exception: another one.
    """
    logger.debug(f"Requested: ({p_index_start};{p_index_stop}), "
                 f"with params {kwargs}")
    html_codes = asyncio.run(
        get_htmls_coro(url, p_index_start, p_index_stop, **kwargs))
    logger.debug("Request was completed successfully")
    return html_codes


def is_http_request_correct(url: str,
                            **kwargs) -> bool:
    """ Whether the request is correct.
    It's correct If there're no exceptions catch.

    :param url: str, request url.
    :param kwargs: request HTTP tags.
    :return: bool, correct the request or not.
    """
    # coro writes logs by itself
    try:
        get_htmls(url, **kwargs)
    except Exception:
        return False
    return True


def whether_result_found(url: str,
                         **kwargs) -> bool:
    """ Whether the page contains results.

    RuntimeError if the request is wrong.

    :param url: str, request url.
    :param kwargs: request HTTP tags.
    :exception RuntimeError: if HTTP request is wrong.
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
    Corpus redirects to the first page if the page at the number doesn't exist.
    Here it's assumed, that the request's correct.

    :param url: str, url.
    :param p_index: int, index of page. Indexing starts with 0.
    :param kwargs: request HTTP tags..
    :return: bool, exists page or not.
    """
    # indexing starts with 0
    start = p_index
    start = start * (start >= 0)
    stop = p_index + 1

    # request is correct → first page exists
    if stop is 1:
        return True

    page_html = get_htmls(url, start, stop, **kwargs)[0]
    soup = bs4.BeautifulSoup(page_html, 'lxml')

    pager = soup.find('p', {'class': 'pager'})
    if pager:
        p_num = pager.b
        if not p_num:
            return False
        p_num = p_num.text
        # page_index from pager should be equal to expected index
        return p_num == str(stop)

    # if there's no pager, but result exists
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
        means the Corpus doesn't redirect to first page).

    :param url: str, request url.
    :param p_count: int, request count of pages.
    :param kwargs: request HTTP tags.
    :return: True if everything's OK, an exception otherwise.
    :exception ValueError: something's wrong.
    """
    # coro writes logs by itself
    try:
        assert whether_result_found(url, **kwargs) is True
    except AssertionError:
        raise ValueError("No result found")
    except RuntimeError:
        raise ValueError("Wrong HTTP request")

    if not does_page_exist(url, p_count - 1, **kwargs):
        raise ValueError("Last page doesn't exist")

    return True
