__all__ = (
    'MainCorpus'
)

import csv
import json
import logging
import random
import string
import time
import webbrowser
from pathlib import Path
from typing import Dict, Callable, List, Any

import bs4

import rnc.corpora_logging as clog
import rnc.corpora_requests as creq
import rnc.examples as expl

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


# Russian National Corpus URL
RNC_URL = "http://processing.ruscorpora.ru/search.xml"


class Subcorpus:
    class Person:
        Pushkin = 'JSONeyJkb2NfYXV0aG9yIjogWyLQkC7QoS4g0J_Rg9GI0LrQuNC9Il19'
        Dostoyevsky = 'JSONeyJkb2NfYXV0aG9yIjogWyLQpC7QnC4g0JTQvtGB0YLQvtC10LLRgdC60LjQuSJdfQ%3D%3D'
        TolstoyLN = 'JSONeyJkb2NfYXV0aG9yIjogWyLQmy7QnS4g0KLQvtC70YHRgtC-0LkiXX0%3D'
        Chekhov = 'JSONeyJkb2NfYXV0aG9yIjogWyLQkC7Qny4g0KfQtdGF0L7QsiJdfQ%3D%3D'
        Gogol = 'JSONeyJkb2NfYXV0aG9yIjogWyLQnS7Qki4g0JPQvtCz0L7Qu9GMIl19'
        Turgenev = 'JSONeyJkb2NfYXV0aG9yIjogWyLQmC7QoS4g0KLRg9GA0LPQtdC90LXQsiJdfQ%3D%3D'

    class Parallel:
        English = 'JSONeyJkb2NfbGFuZyI6IFsiZW5nIl0sICJpc19wYXJhX2JvdGhfcGFpcnMiOiBbdHJ1ZV19'
        Armenian = 'JSONeyJkb2NfbGFuZyI6IFsiYXJtIl0sICJpc19wYXJhX2JvdGhfcGFpcnMiOiBbdHJ1ZV19'
        Bashkir = 'JSONeyJkb2NfbGFuZyI6IFsiYmFzaCJdLCAiaXNfcGFyYV9ib3RoX3BhaXJzIjogW3RydWVdfQ=='
        Belarusian = 'JSONeyJkb2NfbGFuZyI6IFsiYmVsIl0sICJpc19wYXJhX2JvdGhfcGFpcnMiOiBbdHJ1ZV19'
        Bulgarian = 'JSONeyJkb2NfbGFuZyI6IFsiYnVsIl0sICJpc19wYXJhX2JvdGhfcGFpcnMiOiBbdHJ1ZV19'
        Buryatian = 'JSONeyJkb2NfbGFuZyI6IFsiYnVhIl0sICJpc19wYXJhX2JvdGhfcGFpcnMiOiBbdHJ1ZV19'
        Spanish = 'JSONeyJkb2NfbGFuZyI6IFsiZXNwIl0sICJpc19wYXJhX2JvdGhfcGFpcnMiOiBbdHJ1ZV19'
        Italian = 'JSONeyJkb2NfbGFuZyI6IFsiaXRhIl0sICJpc19wYXJhX2JvdGhfcGFpcnMiOiBbdHJ1ZV19'
        # In developing, wait some time...
        # Chinese = ''
        Latvian = 'JSONeyJkb2NfbGFuZyI6IFsibGF2Il0sICJpc19wYXJhX2JvdGhfcGFpcnMiOiBbdHJ1ZV19'
        Lithuanian = 'JSONeyJkb2NfbGFuZyI6IFsibGl0Il0sICJpc19wYXJhX2JvdGhfcGFpcnMiOiBbdHJ1ZV19'
        German = 'JSONeyJkb2NfbGFuZyI6IFsiZ2VyIl0sICJpc19wYXJhX2JvdGhfcGFpcnMiOiBbdHJ1ZV19'
        Polish = 'JSONeyJkb2NfbGFuZyI6IFsicG9sIl0sICJpc19wYXJhX2JvdGhfcGFpcnMiOiBbdHJ1ZV19'
        Ukrainian = 'JSONeyJkb2NfbGFuZyI6IFsidWtyIl0sICJpc19wYXJhX2JvdGhfcGFpcnMiOiBbdHJ1ZV19'
        French = 'JSONeyJkb2NfbGFuZyI6IFsiZnJhIl0sICJpc19wYXJhX2JvdGhfcGFpcnMiOiBbdHJ1ZV19'
        Finnish = 'JSONeyJkb2NfbGFuZyI6IFsiZmluIl0sICJpc19wYXJhX2JvdGhfcGFpcnMiOiBbdHJ1ZV19'
        Czech = 'JSONeyJkb2NfbGFuZyI6IFsiY3plIl0sICJpc19wYXJhX2JvdGhfcGFpcnMiOiBbdHJ1ZV19'
        Swedish = 'JSONeyJkb2NfbGFuZyI6IFsic3ZlIl0sICJpc19wYXJhX2JvdGhfcGFpcnMiOiBbdHJ1ZV19'
        Estonian = 'JSONeyJkb2NfbGFuZyI6IFsiZXN0Il0sICJpc19wYXJhX2JvdGhfcGFpcnMiOiBbdHJ1ZV19'


def create_filename(length: int = 12) -> str:
    """ Create random filename.

    :param length: int, length of result (12 by default).
    :return: str, random symbols.
    """
    name = random.sample(string.ascii_letters, length)
    return ''.join(name)


def create_unique_filename() -> Path:
    """ Create a random unique csv filename,
    means the file doesn't exist.

    :return: Path, unique filename. len = 12.
    """
    path = Path(f"{create_filename()}.csv")
    while path.exists():
        path = path.with_name(f"{create_filename()}.csv")
    return path


def clean_text_up(text: str) -> str:
    """ Remove duplicate spaces from str and strip it.

    :param text: str to clean up.
    :return: str, clean str.
    """
    return ' '.join(text.split()).strip()


def create_doc_url(doc_url: str) -> str:
    """ Create full url to document in Corpus.
    Add https://... to doc.

    :param doc_url: str, doc url to extend.
    :return: str, extended url.
    """
    rnc_url = RNC_URL[:RNC_URL.rindex('/')]
    return f"{rnc_url}/{doc_url}"


def join_with_plus(item: str) -> str:
    """ Split txt and join it with '+'.

    :param item: str, text to convert.
    :return: str, converted text.
    """
    res = item.split()
    return '+'.join(res)


# TODO: additional info from the first corpus page
class Corpus:
    """ Base class for Corpora """
    # default params
    # documents per page
    __DPP = 5
    # sentences per document
    __SPD = 10
    # search format
    __TEXT = 'lexgramm'
    # output format
    __OUT = 'normal'
    # accent on words, without accent by default
    __ACCENT = '0'
    # show order
    __SORT = 'i_grtagging'
    # distance between n and (n + 1) words
    __MIN = 1
    __MAX = 3

    def __init__(self,
                 query: dict or str = None,
                 p_count: int = None,
                 file: str or Path = None,
                 **kwargs) -> None:
        """ There're no checking arguments valid.

        If the file exists, working with a local database.

        :param query: dict of str, words to search;
         {word1: {properties}, word2: {properties}...}.
         If you chose 'lexform' as a 'text' param, you must give here a string.
        :param p_count: int, count of pages to request.
        :param file: str or Path, filename of a local database.
        :keyword dpp: str or int, documents per page.
        :keyword spd: str or int, sentences per document.
        :keyword text: str, search format: 'lexgramm' or 'lexform'.
        :keyword out: str, output format: 'normal' or 'kwic'.
        :keyword kwsz: str or int, count of words in context;
         Optional param if 'out' is 'kwic'.
        :keyword sort: str, sort show order. See docs how to set it.
        :keyword subcorpus: str, subcorpus. See docs how to set it.
        :keyword expand: str, if 'full', all part of doc will be shown.
        :keyword accent: str or int, with accents on words or not:
         1 – with, 0 – without.

        :keyword marker: function, with which found words will be marked.
        """
        # list of examples
        self._data = []
        # http tags to request
        self._params = {}
        # found wordforms with their frequency
        self._found_wordforms = {}
        self._query = {}
        self._p_count = 0
        # type of example should be defined after params init
        # it always should be given
        self._ex_type = kwargs.pop('ex_type', None)
        self._marker = kwargs.pop('marker', None)

        # path to local database
        path = file or create_unique_filename()
        path = f"{path}{'.csv' * (not str(path).endswith('.csv'))}"

        # to these files the data and req params will be dumped
        self._csv_path = Path(path)
        self._config_path = Path(f"{self._csv_path.stem}.json")

        if self._csv_path.exists():
            try:
                self._load()
            except FileExistsError as e:
                logger.exception(f"There's no config file found")
                raise e
            self._page_parser_and_ex_type()
            return

        self._query = query
        self._p_count = p_count
        if p_count <= 0:
            msg = "Page count must be > 0"
            logger.error(msg)
            raise ValueError(msg)

        # base params
        self._params['env'] = 'alpha'
        self._params['api'] = '1.0'
        self._params['lang'] = 'en'

        self._params['dpp'] = kwargs.pop('dpp', None) or self.__DPP
        self._params['spd'] = kwargs.pop('spd', None) or self.__SPD
        self._params['text'] = kwargs.pop('text', None) or self.__TEXT
        self._params['out'] = kwargs.pop('out', None) or self.__OUT
        self._params['sort'] = kwargs.pop('sort', None) or self.__SORT

        accent = kwargs.pop('accent', None) or self.__ACCENT
        accent = int(accent)
        self._params['nodia'] = int(not accent)

        if self.params['out'] == 'kwic' and 'kwsz' in kwargs:
            self._params['kwsz'] = kwargs.pop('kwsz')

        if 'subcorpus' in kwargs:
            self._params['mycorp'] = kwargs.pop('subcorpus')
        if 'expand' in kwargs:
            self._params['expand'] = kwargs.pop('expand')

        self._query_to_http()

        # parsing depends on 'out' value
        self._page_parser = None
        self._page_parser_and_ex_type()

    @property
    def data(self) -> List:
        """
        :return: list of examples.
        """
        return self._data

    @property
    def query(self) -> Dict[str, dict] or str:
        """
        :return: dict or str, requested items.
        """
        return self._query

    @property
    def forms_in_query(self) -> List[str]:
        """
        :return: list of str, requested words.
        """
        req = self.query
        if isinstance(req, str):
            return [req]
        return list(req.keys())

    @property
    def p_count(self) -> int:
        """
        :return: int, requested count of pages.
        """
        return self._p_count

    @property
    def file(self) -> Path:
        """
        :return: Path, path to local database file.
        """
        return self._csv_path

    @property
    def marker(self) -> Callable:
        """
        :return: function to mark found wordforms.
        """
        return self._marker

    @property
    def params(self) -> dict:
        """
        :return: dict of HTTP params.
        """
        return self._params

    @property
    def found_wordforms(self) -> dict:
        """ Get info about found wordforms, {form: frequency}.

        :return: dict of str, found wordforms and their frequency.
        """
        return self._found_wordforms

    @property
    def url(self) -> str:
        """ Return url, first page of Corpus results.

        :return: str, url.
        """
        params = '&'.join(
            f"{key}={val}"
            for key, val in self.params.items()
        )
        return f"{RNC_URL}?{params}"

    @property
    def ex_type(self) -> Any:
        """
        :return: example type of the Corpus.
        """
        return self._ex_type

    def _page_parser_and_ex_type(self) -> None:
        """ Add 'parser' and 'ex_type' params.
        They are depended on 'out' tag.

        :return: None
        """
        if self.params['out'] == 'normal':
            # ex_type is defined above in this case
            self._page_parser = self._parse_page_normal
        elif self.params['out'] == 'kwic':
            self._page_parser = self._parse_page_kwic
            self._ex_type = expl.KwicExample

    def open_url(self) -> None:
        """ Open first page of Coprus results in the new
        tab of the default browser.

        :return: None.
        :exception ValueError: if url is wrong.
        :exception: if sth went wrong.
        """
        try:
            webbrowser.open_new_tab(self.url)
        except Exception as e:
            logger.exception(
                f"Error while opening doc with url: {self.url}")
            raise e

    def add_pages(self,
                  p_count: int) -> None:
        """ Add new pages in (last_p_count; last_p_count + new_p_count)
        (Needed for working with local database)
        """
        # TODO
        pass

    def request_examples(self) -> None:
        """ Request examples, parse them and update the data.

        If there're no results found, last page doesn't exist,
        params or query is wrong then exception.

        :return: None.
        :exception aiohttp.ClientResponseError:
        :exception aiohttp.ClientConnectionError:
        :exception aiohttp.InvalidURL:
        :exception aiohttp.ServerTimeoutError:
        :exception Exception: another one.

        :exception RuntimeError: if the data still exist.
        """
        if self.data:
            logger.error("Tried to request new examples, however data exist")
            raise RuntimeError("Data still exist")

        try:
            creq.is_request_correct(RNC_URL, self.p_count, **self.params)
        except Exception as e:
            msg = f"Query = {self.forms_in_query}, {self.p_count}, {self.params}"
            logger.exception(msg)
            raise e

        start, stop = 0, self.p_count
        coro_start = time.time()
        htmls = creq.get_htmls(RNC_URL, start, stop, **self.params)
        logger.info(f"Coro executing time: {time.time() - coro_start:.2f}")

        try:
            parsing_start = time.time()
            parsed = self._parse_all_pages(htmls)
            parsing_stop = time.time()
        except Exception as e:
            logger.exception(f"Error while parsing, query = {self.params}")
            raise e
        else:
            logger.info(f"Parsing time: {parsing_stop - parsing_start:.2f}")
            logger.info(f"Overall time: {parsing_stop - coro_start:.2f}")
            self._data = parsed[:]

    def _data_to_csv(self) -> None:
        """ Dump the data to csv file.
        Here it's assumed that the data exists.

        :return: None.
        """
        data = [i.items for i in self.data]
        columns = self[0].columns
        with self.file.open('w', encoding='utf-16', newline='') as f:
            writer = csv.writer(
                f, delimiter='\t', quotechar='\n', quoting=csv.QUOTE_MINIMAL)
            writer.writerows([columns] + data)

    def _params_to_json(self) -> None:
        """ Write the request params: query,
        p_count and http tags to json file.

        Here it's assumed that these params exist.

        :return: None.
        """
        to_write = {
            'query': self.query,
            'p_count': self.p_count,
            'params': self.params
        }
        with self._config_path.open('w', encoding='utf-16') as f:
            json.dump(to_write, f, indent=4, ensure_ascii=False)

    def copy(self) -> Any:
        """
        :return: copied object.
        """
        return self[:]

    def dump(self) -> None:
        """ Write the data to csv file, request params to json file.

        :return: None.
        :exception RuntimeError: If there're no data, params or files exist.
        """
        if not self.data:
            logger.error("Tried to write empty data to file")
            raise RuntimeError("There're no data to write")
        if not (self.query and self.p_count and self.params):
            logger.error("Tried to write empty config to file")
            raise RuntimeError("There're no data to write")
        if self._config_path.exists() and self.file.exists():
            logger.error("Tried to write data, however it even exists")
            raise RuntimeError("Files with data still exist")

        self._data_to_csv()
        self._params_to_json()

        logger.debug(
            f"Data was wrote to files: {self.file} and {self._config_path}")

    def sort(self,
             **kwargs) -> None:
        """ Sort the data by using a key.

        :keyword key: func to sort, called to Example objects, by default – len.
        :keyword reverse: bool, whether the data'll sort in reversed order,
         by default – False.
        :return None.
        :exception TypeError: if the key is uncallable.
        """
        key = kwargs.pop('key', lambda x: len(x))
        reverse = kwargs.pop('reverse', False)

        if not callable(key):
            logger.error("Given uncallable key to sort")
            raise TypeError("Sort key must be callable")
        self._data.sort(key=key, reverse=reverse)

    def pop(self, index: int) -> Any:
        """ Remove and return element from data at the index.

        :param index: int, index of the element.
        :return: Example object.
        """
        return self._data.pop(index)

    def shuffle(self) -> None:
        """ Shuffle list of examples.
        :return: None.
        """
        random.shuffle(self._data)

    def _get_ambiguation(self,
                         tag: bs4.element.Tag) -> str:
        """ Get pretty ambiguation from example.

        :param tag: bs4.element.Tag, example.
        :return: str, 'disambiguated' or 'not disambiguated' or 'Not found'.
        """
        ambiguation = (tag.find('span', {'class': 'on'}) or
                       tag.find('span', {'class': 'off'}))
        if not ambiguation:
            return 'Not found'
        ambiguation = ambiguation.text.strip()
        # here ambiguation like '[...]'
        ambiguation = ambiguation[1:-1].strip()
        return ambiguation

    def _get_text(self,
                  tag: bs4.element.Tag) -> str:
        """ Get pretty text from example and remove
        from there duplicate spaces.

        Here it's assumed, that all examples have text.

        :param tag: bs4.element.Tag, example.
        :return: str, text.
        """
        # using 'findall' method removes punctuation marks
        txt = tag.get_text()
        # remove duplicate spaces
        return clean_text_up(txt)

    def _get_doc_url(self,
                     tag: bs4.element.Tag) -> str:
        """ Get pretty doc url from example.

        :param tag: bs4.element.Tag, example.
        :return: str, doc url or 'Not found'.
        """
        doc_url = tag.a
        if not doc_url:
            return 'Not found'
        doc_url = doc_url.attrs['href']
        return create_doc_url(doc_url)

    def _get_source(self,
                    tag: bs4.element.Tag) -> str:
        """ Get pretty source from example.

        :param tag: bs4.element.Tag, example.
        :return: str, examples source or 'Not found'.
        """
        src = tag.find('span', {'class': 'doc'})
        if not src:
            return "Not found"
        src = clean_text_up(src.text)
        # here src like '[...]'
        src = src[1:-1].strip()
        return src

    # TODO: probably, converting the symbols to their code doesn't needed
    def _parse_lexgramm_params(self,
                               params: dict or str,
                               join_inside_symbol: str,
                               with_braces: bool = False) -> str:
        """ Convert lexgramm params such as
        gramm and flags to str for HTTP request.

        :param params: dict, params to convert.
        :param join_inside_symbol: str, symbol to join params inside.
        :param with_braces: bool, whether the braces will added around the params.
        :return: str, joined with '%2C' params.
        """
        if not (isinstance(params, (str, dict)) and ' ' not in params):
            msg = "Param must be str without spaces or dict"
            logger.error(msg)
            raise ValueError(msg)
        # let the user to give only one param:
        # {'word': {'gramm': 'acc', 'flags': 'bmark'}}
        if isinstance(params, str):
            return params

        res = []
        for val in params.values():
            if isinstance(val, (str, int)):
                val = [str(val)]

            if isinstance(val, list):
                val = [i.replace(':', '%3A') for i in val]
                item = f"{'%28' * with_braces}" \
                       f"{join_inside_symbol.join(val)}" \
                       f"{'%29' * with_braces}"
                res += [item]
            else:
                msg = "One should give to tags only str, list or int"
                logger.error(msg)
                raise ValueError(msg)
        return '%2C'.join(res)

    def _query_to_http(self) -> None:
        """ Convert the query to HTTP tags, add them to params.

        :return: None.
        :exception ValueError: if wrong type given.
        """
        if self.params['text'] == 'lexform':
            query = self._query
            if isinstance(query, str):
                self._params['req'] = join_with_plus(query)
                return
            msg = "One must give str as a query if search is 'lexform'"
            logger.error(msg)
            raise ValueError(msg)

        # in lexgramm search one word may be too
        if isinstance(self.query, str):
            self._params['lex1'] = join_with_plus(self.query)
            return

        word_num = 1
        # words and their params
        for word, params in self.query.items():
            # add distance
            if word_num > 1:
                mmin = f'min{word_num}'
                mmax = f'max{word_num}'
                # given or default values
                self._params[mmin] = params.get(mmin, None) or self.__MIN
                self._params[mmax] = params.get(mmax, None) or self.__MAX
            self._params[f"lex{word_num}"] = join_with_plus(word)

            # grammar properties
            gramm = params.get('gramm', '')
            if gramm:
                try:
                    gram_props = self._parse_lexgramm_params(gramm, '%7C', True)
                except Exception as e:
                    raise e
                self._params[f"gramm{word_num}"] = gram_props

            # additional properties
            flags = params.get('flags', '')
            if flags:
                try:
                    flag_prop = self._parse_lexgramm_params(flags, '+')
                except Exception as e:
                    raise e
                self._params[f"flags{word_num}"] = flag_prop

            # TODO: semantic properties
            sem = params.get('sem', '')
            if sem:
                try:
                    sem_prop = self._parse_lexgramm_params(sem, '')
                except Exception as e:
                    raise e
                # self.__params фильтр1 и фильтр2

            word_num += 1

    def _add_wordform(self,
                      forms: List[str]) -> None:
        """ Add found wordforms to counter. Low and strip items.

        :param forms: list of str, wordforms to add.
        :return: None.
        """
        if not forms:
            return

        forms = [
            clean_text_up(form).lower()
            for form in forms
        ]

        for form in forms:
            self._found_wordforms[form] = self.found_wordforms.get(form, 0) + 1

    def _parse_doc(self,
                   doc: bs4.element.ResultSet) -> List:
        """ Parse the doc to list of Examples.

        Parsing depends on subcorpus, the method redefined at descendants.
        """
        pass

    def _parse_page_kwic(self,
                         page: str) -> List[expl.KwicExample]:
        """ Parse page if 'out' is 'kwic'.

        :param page: str, html code of page to parse.
        :return: list of examples.
        :exception ValueError: if the content not found.
        """
        soup = bs4.BeautifulSoup(page, 'lxml')
        res = []

        content = soup.find('table', {'align': 'left'})
        if not content:
            msg = "Content is None, this behavior is undefined, contact the developer"
            logger.error(msg)
            raise ValueError(msg)

        nobr = content.find_all('nobr')
        if len(nobr) % 3:
            logger.warning("Len of nobr tags list % 3 != 0")

        for left, center, right in zip(nobr[::3], nobr[1::3], nobr[2::3]):
            l_txt = clean_text_up(left.text)
            c_txt = clean_text_up(center.text)
            # remove ←…→ symbol too
            r_txt = clean_text_up(right.text)[:-4]

            found_wordforms = self._find_searched_words(left)
            found_wordforms += self._find_searched_words(center)
            found_wordforms += self._find_searched_words(right)
            self._add_wordform(found_wordforms)

            try:
                src = right.a.attrs['msg'].strip()
                url = right.a.attrs['href']
            except Exception:
                logger.exception("Source or url not found")
            else:
                url = create_doc_url(url)

                new_ex = expl.KwicExample(
                    l_txt, c_txt, r_txt, src, found_wordforms, url)
                new_ex.mark_found_words(self.marker)
                res += [new_ex]
        return res

    def _parse_page_normal(self,
                           page: str) -> List:
        """ Parse page if 'out' is 'normal'.

        :param page: str, html code to parse.
        :return: list of examples.
        """
        soup = bs4.BeautifulSoup(page, 'lxml')
        res = []

        for doc in soup.find_all('ul'):
            li = doc.find_all('li')
            try:
                parsed_doc = self._parse_doc(li)
            except Exception:
                logger.exception("Error while parsing doc")
            else:
                res += parsed_doc

        return res

    def _parse_all_pages(self,
                         pages: List[str]) -> List:
        """ Parse all pages.

        :param pages: list of str, html codes of the pages.
        :return: list of examples.
        """
        parsed = [self._page_parser(page) for page in pages]
        return sum(parsed, [])

    def _find_searched_words(self,
                             tag: bs4.element.Tag) -> List[str]:
        """ Get searched words from tag, they are marked with 'g-em'
        parameter in the class name. Strip them.

        :param tag: bs4.element.Tag, tag with result.
        :return: list of string, words to which request was.
        """
        # params of the classes and word if 'class' is
        class_params = [
            (i.attrs.get('class', ''), i.text)
            for i in tag.contents
            if isinstance(i, bs4.element.Tag)
        ]
        # searched words are marked by class parameter 'g-em'
        searched_words = [
            i[1].strip()
            for i in class_params
            if 'g-em' in i[0]
        ]
        return searched_words

    def _load_data(self) -> List:
        """ Load data from csv file.

        :return: list of examples.
        """
        with self.file.open('r', encoding='utf-16') as f:
            reader = csv.reader(f, delimiter='\t', quotechar='\n')

            # first row contains headers
            data = [i for i in reader][1:]
        return [self._ex_type(*i) for i in data]

    def _load_params(self) -> Dict:
        """ Load request params from json file.

        :return: json dicc.
        """
        with self._config_path.open('r', encoding='utf-16') as f:
            return json.load(f)

    def _load(self) -> None:
        """ Load data and params from local databases.

        :return: None.
        :exception FileExistsError: if the file doesn't exist.
        """
        if not (self._csv_path.exists() and self._config_path.exists()):
            msg = "Data and config file must exist together"
            logger.error(msg)
            raise FileExistsError(msg)

        params = self._load_params()
        self._query = params.get('query', None)
        self._p_count = params.get('p_count', None)
        self._params = params.get('params', None)

        # TODO
        # assert self.params['mode'] == self.__MODE

        # these params must be defined here too
        self._page_parser_and_ex_type()

        self._data = self._load_data()

    def __repr__(self) -> str:
        """ Format:
                Classname
                Length
                Database filename
                Request params
                Pages count
                Request
                Marker
        :return: str with the format.
        """
        res = f"{self.__class__.__name__}\n" \
              f"{len(self)}\n" \
              f"{self.file}\n" \
              f"{self.params}\n" \
              f"{self.p_count}\n" \
              f"{self.query}\n" \
              f"{self.marker}"
        return res

    def __str__(self) -> str:
        """
        :return: str, classname, length and enumerated examples.
        """
        res = f"Russian National Corpus (https://ruscorpora.ru)\n" \
              f"Class: {self.__class__.__name__}, len = {len(self)}\n" \
              f"{self.p_count} pages requested\n\n"
        res += '\n\n'.join(
            f"{num}.\n{str(example)}"
            for num, example in enumerate(self, 1)
        )
        return res

    def __len__(self) -> int:
        """
        :return: int, count of examples.
        """
        return len(self.data)

    def __bool__(self) -> bool:
        """
        :return: bool, whether data exist.
        """
        return bool(self.data)

    def __call__(self) -> None:
        """ Request examples, parse them and update the data.

        If there're no results found, last page doesn't exist,
        params or query is wrong then exception.

        :return: None.
        :exception aiohttp.ClientResponseError:
        :exception aiohttp.ClientConnectionError:
        :exception aiohttp.InvalidURL:
        :exception aiohttp.ServerTimeoutError:
        :exception Exception: another one.

        :exception RuntimeError: if the data still exist.
        """
        self.request_examples()

    def __iter__(self) -> iter:
        """
        :return: iter, iterator for data.
        """
        return iter(self.data)

    def __getattr__(self,
                    item: str) -> str or int or List or None:
        """ Get request param.

        :param item: item, param name.
        :return: param value or None if it doesn't exist.
        """
        return self.params.get(item, None)

    def __getitem__(self,
                    item: int or slice) -> Any:
        """ Get example from data or create
        new corpus obj with sliced data.

        :param item: int or slice.
        :return: one example or new obj with the same class and sliced data.
        :exception TypeError: if wrong type given.
        """
        if not isinstance(item, (int, slice)):
            logger.error("Int or slice expected")
            raise TypeError("Int or slice expected")

        if isinstance(item, int):
            return self.data[item]

        new_data = self.data[item]
        new_obj = self.__class__(
            self.query, self.p_count, self.file,
            **self.params, marker=self.marker)
        new_obj._data = new_data.copy()
        return new_obj

    def __copy__(self) -> Any:
        """ Copy self.

        :return: copied obj.
        """
        return self[:]

    def __lt__(self, other) -> bool:
        """ <
        :param other: int or another Corpus obj.
        :return: whether len(self) < len(other).
        :exception TypeError: if wrong type given.
        """
        if isinstance(other, int):
            return len(self) < other
        elif isinstance(other, self.__class__):
            return len(self) < len(other)
        else:
            msg = f"Int or {self.__class__.__name__} expected"
            logger.error(msg)
            raise TypeError(msg)

    def __le__(self, other) -> bool:
        """ <=
        :param other: int or another Corpus obj.
        :return: whether len(self) <= len(other).
        :exception TypeError: if wrong type given.
        """
        return self < other or self == other

    def __eq__(self, other) -> bool:
        """ ==
        :param other: int or another Corpus obj.
        :return: whether len(self) == len(other).
        :exception TypeError: if wrong type given.
        """
        if isinstance(other, int):
            return len(self) == other
        elif isinstance(other, self.__class__):
            return len(self) == len(other)
        else:
            msg = f"int or {self.__class__.__name__} expected"
            logger.error(msg)
            raise TypeError(msg)

    def __ne__(self, other) -> bool:
        """ !=
        :param other: int or another Corpus obj.
        :return: whether len(self) != len(other).
        :exception TypeError: if wrong type given.
        """
        return not (self == other)

    def __gt__(self, other) -> bool:
        """ >
        :param other: int or another Corpus obj.
        :return: whether len(self) > len(other).
        :exception TypeError: if wrong type given.
        """
        return not (self == other or self < other)

    def __ge__(self, other) -> bool:
        """ >=
        :param other: int or another Corpus obj.
        :return: whether len(self) >= len(other).
        :exception TypeError: if wrong type given.
        """
        return self == other or self > other


class MainCorpus(Corpus):
    def __init__(self,
                 *args,
                 **kwargs):
        """ There're no checking arguments valid.

        If the file exists, working with a local database.

        :param query: dict of str, words to search;
         {word1: {properties}, word2: {properties}...}.
         If you chose 'lexform' as a 'text' param, you must give here a string.
        :param p_count: int, count of pages to request.
        :param f_path: str or Path, filename of a local database.
        :keyword dpp: str or int, documents per page.
        :keyword spd: str or int, sentences per document.
        :keyword text: str, search format: 'lexgramm' or 'lexform'.
        :keyword out: str, output format: 'normal' or 'kwic'.
        :keyword kwsz: str or int, count of words in context;
         Optional param if 'out' is 'kwic'.
        :keyword sort: str, sort show order. See docs how to set it.
        :keyword subcorpus: str, subcorpus. See docs how to set it.
        :keyword expand: str, if 'full', all part of doc will be shown.
        :keyword accent: str or int, with accents on words or not:
         1 – with, 0 – without.

        :keyword marker: function, with which found words will be marked.
        """
        super().__init__(*args, **kwargs, ex_type=expl.MainExample)
        self._params['mode'] = 'main'

    def _parse_doc(self,
                   doc: bs4.element.ResultSet) -> List[expl.MainExample]:
        """ Parse document to list of examples.

        :param doc: bs4.element.ResultSet,
        """
        if not doc:
            logger.info(f"Empty doc found, params: {self.params}")
            return []

        res = []
        # one doc – one source
        src = self._get_source(doc[0])
        for ex in doc:
            txt = self._get_text(ex)
            txt = txt[:txt.index(src)]
            txt = txt[:txt.rindex('[')].strip()

            doc_url = self._get_doc_url(ex)
            ambiguation = self._get_ambiguation(ex)

            found_words = self._find_searched_words(ex)
            self._add_wordform(found_words)

            new_ex = self._ex_type(txt, src, ambiguation, found_words, doc_url)
            new_ex.mark_found_words(self.marker)
            res += [new_ex]

        return res


class NGrams(Corpus):
    # env = sas1_2
    pass


class BiGrams(NGrams):
    pass


class ThreeGrams(NGrams):
    pass


class FourGrams(NGrams):
    pass


class FiveGrams(NGrams):
    pass


class SyntaxCorpus(Corpus):
    pass


class Paper2000Corpus(MainCorpus):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._params['mode'] = 'paper'
        self._ex_type = expl.Paper2000Example


class PaperRegionalCorpus(MainCorpus):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._params['mode'] = 'regional'
        self._ex_type = expl.PaperRegionalExample


class ParallelCorpus(Corpus):
    # TODO: working with csv
    def __init__(self, *args, **kwargs):
        """ There're no checking arguments valid.

        If the file exists, working with a local database.

        :param query: dict of str, words to search;
         {word1: {properties}, word2: {properties}...}.
         If you chose 'lexform' as a 'text' param, you must give here a string.
        :param p_count: int, count of pages to request.
        :param f_path: str or Path, filename of a local database.
        :keyword dpp: str or int, documents per page.
        :keyword spd: str or int, sentences per document.
        :keyword text: str, search format: 'lexgramm' or 'lexform'.
        :keyword out: str, output format: 'normal' or 'kwic'.
        :keyword kwsz: str or int, count of words in context;
         Optional param if 'out' is 'kwic'.
        :keyword sort: str, sort show order. See docs how to set it.
        :keyword subcorpus: str, subcorpus. See docs how to set it.
        :keyword expand: str, if 'full', all part of doc will be shown.
        :keyword accent: str or int, with accents on words or not:
         1 – with, 0 – without.

        :keyword marker: function, with which found words will be marked.
        """
        super().__init__(*args, **kwargs, ex_type=expl.ParallelExample)
        self._params['mode'] = 'para'

    def _parse_example(self,
                       tag: bs4.element.Tag):
        """ Parse one sentence

        :param tag: bs4.element.Tag, sentence to parse.
        """
        lang = tag.span['l'].strip()

        src = self._get_source(tag)
        ambiguation = self._get_ambiguation(tag)
        doc_url = self._get_doc_url(tag)
        txt = self._get_text(tag)
        # remove source from text
        txt = txt[:txt.index(src)]
        txt = txt[:txt.rindex('[')].strip()

        found_words = self._find_searched_words(tag)

        return lang, txt, src, doc_url, ambiguation, found_words

    def _best_src(self,
                  f_src: str,
                  s_src: str) -> str:
        if '|' in s_src:
            return s_src
        return f_src

    def _parse_doc(self,
                   doc: bs4.element.Tag) -> List:
        # TODO: NamedTuple
        res = []
        for fst, sec in zip(doc[::2], doc[1::2]):
            f_lang, f_txt, f_src, f_url, f_amb, f_fw = self._parse_example(fst)
            s_lang, s_txt, s_src, s_url, s_amb, s_fw = self._parse_example(sec)

            src = self._best_src(f_src, s_src)
            fw = f_fw + s_fw

            # TODO: fix it
            assert f_lang != s_lang, "Languages should be different"

            self._add_wordform(fw)

            new_ex = self._ex_type(
                {f_lang: f_txt, s_lang: s_txt}, src, f_amb, fw, f_url)
            new_ex.mark_found_words(self.marker)
            res += [new_ex]

        return res

    def __str__(self) -> str:
        res = '\n\n'.join(
            f"{num}.\n{i}"
            for num, i in enumerate(self.data, 1)
        )
        return res


class RusGerParaCorpus(ParallelCorpus):
    # mode = para_rus_ger
    pass


class MultilingualParaCorpus(ParallelCorpus):
    # mode = multi
    pass


class LearningCorpus(Corpus):
    def __init__(self,
                 *args,
                 **kwargs):
        super().__init__(*args, **kwargs)
        self.params['mode'] = 'school'

    pass


# TODO: add gram tags to docs
class DialectCorpus(MainCorpus):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._params['mode'] = 'dialect'
        self._ex_type = expl.DialectExample


# save lines
class PoetryCorpus(Corpus):
    pass


class SpokenCorpus(MainCorpus):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._params['mode'] = 'spoken'
        self._ex_type = expl.SpokenExample


class AccentologyCorpus(MainCorpus):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._params['mode'] = 'accent'
        self._ex_type = expl.AccentologyExample


class MultimediaCorpus(Corpus):
    pass


class MultiparkCorpus(Corpus):
    pass


class HistoricalCorpus(Corpus):
    pass
