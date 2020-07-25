""" Module for requesting to URL and get page's html code """
__all__ = 'get_htmls', 'is_request_correct'

import asyncio
import logging
from typing import List

import aiohttp
import bs4

import src.corpora_logging as clog

log_file = clog.log_folder / f"{__name__}.log"
formatter = clog.create_formatter()

stream_handler = clog.create_stream_handler(
    level=logging.WARNING,
    formatter=formatter)
file_handler = clog.create_file_handler(
    log_path=log_file,
    formatter=formatter,
    delay=True,
    encoding='utf-8')

logger = clog.create_logger(
    __name__, logging.DEBUG, file_handler, stream_handler)


async def fetch(url: str,
                ses: aiohttp.ClientSession,
                **kwargs) -> str:
    """ Coro, obtaining page's html code. There's ClientTimeout.

    If response.status == 429 sleep and try again.
    If response.status != 429 and != 200, raise an exception.

    :param url: string, URL to get its html code.
    :param ses: aiohttp.ClientSession.
    :param kwargs: HTTP tags.
    :return: html code, decoded to UTF-8.
    """
    wait = 24
    t_out = aiohttp.ClientTimeout(wait + 1)
    async with ses.get(url, params=kwargs, timeout=t_out) as resp:
        if resp.status == 200:
            return await resp.text('utf-8')

        if resp.status != 429:
            resp.raise_for_status()

        await asyncio.sleep(wait)
        return await fetch(url, ses, **kwargs)


async def get_htmls_coro(url: str,
                         p_index_start: int,
                         p_index_stop: int,
                         **kwargs) -> List[str]:
    """ Coro doing requests and catching exceptions.

    URLs will be created for i in range(p_index_start, p_index_stop),
    HTTP tag 'p' (page) is i.

    :param url: str, URL. It must start with http(s)://
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

        html_codes = []
        while True:
            done, pending = await asyncio.wait(tasks)
            for future in done:
                try:
                    page_code = future.result()
                except aiohttp.ClientResponseError as e:
                    # 5.., 404 etc
                    logger.exception(e)
                    raise e
                except aiohttp.ClientConnectionError as e:
                    # there's no connection or access to the site
                    logger.exception(e)
                    raise e
                except aiohttp.InvalidURL as e:
                    # wrong url or params
                    logger.exception(e)
                    raise e
                except aiohttp.ServerTimeoutError as e:
                    # timeout
                    logger.exception(e)
                    raise e
                except Exception as e:
                    # another error
                    logger.exception(e)
                    raise e
                else:
                    html_codes += [page_code]
            # TODO: return here?
            return html_codes


def get_htmls(url: str,
              p_index_start: int = 0,
              p_index_stop: int = 1,
              **kwargs) -> List[str]:
    """ Run coro, get html codes of the pages.

    URLs will be created for i in range(p_index_start, p_index_stop),
     HTTP tag 'p' (page) is i.

    :param url: str, URL. It must start with http(s)://
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
    try:
        # coro writes log if the request if wrong
        get_htmls(url, **kwargs)
    except Exception:
        return False
    return True


def whether_result_found(url: str,
                         **kwargs) -> bool:
    """ Whether the page contains results.

    :param url: str, request url.
    :param kwargs: request HTTP tags.
    """
    page_html = get_htmls(url, **kwargs)[0]
    soup = bs4.BeautifulSoup(page_html, 'lxml')

    # TODO: сузить круг поиска
    content = soup.find('div', {'class': 'content'}).text
    res_msg = ('По этому запросу ничего не найдено.' in content or
               'No results match the search query.' in content)
    return not res_msg


def does_page_exist(url: str,
                    p_index: int,
                    **kwargs) -> bool:
    """ Whether a page at the index exists. It means, the number
    of the page in 'pager' is equal to expected index.
    Here it's assumed, that the request's correct.

    :param url: str, url.
    :param p_index: int, index of page. Indexing starts with 0.
    :param kwargs: request HTTP tags..
    :return: bool, exists page or not.
    """
    # indexing starts with 0
    start = p_index
    start = start * (start >= 0)
    stop = (p_index + 1) or 1

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
    # requesting coro writes log with exceptions by itself
    if not is_http_request_correct(url, **kwargs):
        raise ValueError("Wrong http req")

    if not whether_result_found(url, **kwargs):
        raise ValueError("No results found")

    if not does_page_exist(url, p_count - 1, **kwargs):
        raise ValueError("Last page doesn't exist")

    return True
