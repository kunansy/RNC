__all__ = (
    'MainExample',
    'SyntaxExample',
    'Paper2000Example',
    'PaperRegionalExample',
    'ParallelExample',
    'TutoringExample',
    'DialectExample',
    'PoetryExample',
    'SpokenExample',
    'AccentologyExample',
    'MultimediaExample',
    'MultiparkExample',
    'HistoricalExample',
    'KwicExample'
)

import logging
import re
import webbrowser
from typing import List, Callable, Dict

import rnc.corpora_logging as clog

log_file = clog.log_folder / f"{__name__}.log"
formatter = clog.create_formatter()

stream_handler = clog.create_stream_handler(formatter=formatter)
file_handler = clog.create_file_handler(
    log_path=log_file, formatter=formatter)

logger = clog.create_logger(
    __name__, logging.DEBUG, file_handler, stream_handler)


def mark_found_words(txt: str,
                     words: List[str],
                     marker: Callable) -> str:
    """ Mark words in the text.

    :param txt: str, text.
    :param words: list of str, words to mark.
    :param marker: callable, function to mark words with it.
    :return: str with marked words.
    """
    if marker is None:
        return txt

    for word in words:
        txt = re.sub(fr'\b{word}\b', marker(word), txt)
    return txt


# TODO
class TextInfo:
    pass


class Example:
    """ Base examples class """
    __slots__ = (
        '__txt', '__src', '__doc_url',
        '__ambiguation', '__found_wordforms')

    def __init__(self,
                 txt: str,
                 src: str,
                 ambiguation: str,
                 found_wordforms: List[str] or str,
                 doc_url: str) -> None:
        """
        :param txt: str, example's text.
        :param src: str, example's source.
        :param ambiguation: str, example's ambiguation.
        :param found_wordforms: list of str or str joined with ', ',
        example's found wordforms.
        :param doc_url: str, example's url.
        :return: None.
        """
        self.__txt = txt
        self.__src = src
        self.__ambiguation = ambiguation
        self.__doc_url = doc_url

        wf = found_wordforms or []
        if isinstance(wf, str):
            wf = found_wordforms.split(', ')
        self.__found_wordforms = wf

    @property
    def txt(self) -> str:
        """
        :return: str, example's text.
        """
        return self.__txt

    @property
    def src(self) -> str:
        """
        :return: str, example's source.
        """
        return self.__src

    @property
    def ambiguation(self) -> str:
        """
        :return: str, example's ambiguation.
        """
        return self.__ambiguation

    @property
    def doc_url(self) -> str:
        """
        :return: str, example's URL.
        """
        return self.__doc_url

    @property
    def found_wordforms(self) -> List[str]:
        """
        :return: list of str, example's found wordforms.
        """
        return self.__found_wordforms

    @property
    def columns(self) -> List[str]:
        """ For csv writing.

        :return: list of str, names of columns.
        """
        return list(self.data.keys()) + ['URL']

    @property
    def items(self) -> List[str or list]:
        """ For csv writing.

        :return: list of str or list, values of columns.
        """
        # ATTENTION:
        # these order must be the same as in the constructor
        return list(self.data.values()) + [self.doc_url]

    @property
    def data(self) -> Dict:
        """ Found wordforms joined with ', '.

        :return: dict with fields names and their values.
        There're all fields except for doc_url.
        """
        data = {
            'text': self.txt,
            'source': self.src,
            'ambiguation': self.ambiguation,
            'found wordforms': ', '.join(self.found_wordforms)
        }
        return data

    @txt.setter
    def txt(self, other) -> None:
        """ Set text.

        :return: None.
        """
        self.__txt = other

    @ambiguation.setter
    def ambiguation(self, other) -> None:
        """ Set ambiguation.

        :return: None.
        """
        self.__ambiguation = other

    def open_doc(self) -> None:
        """ Open the doc in the new tab of the default browser.

        :return: None.
        :exception ValueError: URL is not like 'http...'
        :exception: if something's wrong.
        """
        if not self.doc_url.startswith('http'):
            logger.exception(
                f"Tried to open doc with wrong url: {self.doc_url}")
            raise ValueError(f"Wrong URL: {self.doc_url}")
        try:
            webbrowser.open_new_tab(self.doc_url)
        except Exception:
            logger.exception(
                f"Error while opening doc with url: {self.doc_url}")
            raise

    def mark_found_words(self,
                         marker: Callable) -> None:
        """ Mark found wordforms in the text with marker.

        :param marker: function to mark found wordforms.
        :return: None.
        """
        self.__txt = mark_found_words(self.txt, self.found_wordforms, marker)

    def __str__(self) -> str:
        """ Str format depends on the descendant.

        :return: this str.
        """
        res = '\n'.join(
            f"{key.upper()}: {val}"
            for key, val in self.data.items()
        )
        return res

    def __repr__(self) -> str:
        """ Str format depends on the descendant.

        :return: this str.
        """
        fields = '\n'.join(
            f"{key}: {val}"
            for key, val in self.data.items()
        )
        url = f"URL: {self.doc_url}"
        return f"{fields}\n{url}"

    def __hash__(self) -> int:
        """ Hash str with all example fields.

        :return: int, hash.
        """
        return hash(repr(self))

    def __bool__(self) -> bool:
        """ .
        :return: bool, whether fields (expect for url) exist
        """
        return all(val for val in self.data.values())


class KwicExample(Example):
    __slots__ = '__left', '__center', '__right'

    def __init__(self,
                 left: str,
                 center: str,
                 right: str,
                 src: str,
                 found_wordforms: List[str] or str,
                 doc_url: str) -> None:
        """ There's no ambiguation, it set with ''.

        :param left: str, example's left context.
        :param center: str, example's center context.
        :param right: str, example's right context.
        :param src: str, example's source.
        :param found_wordforms: list of str or str, example's found wordforms.
        :param doc_url: str, example's URL.
        """
        self.__left = left
        self.__center = center
        self.__right = right
        super().__init__(self.txt, src, '', found_wordforms, doc_url)

    @property
    def left(self) -> str:
        """
        :return: str, example's left context.
        """
        return self.__left

    @property
    def center(self) -> str:
        """
        :return: str, example's center context.
        """
        return self.__center

    @property
    def right(self) -> str:
        """
        :return: str, example's right context.
        """
        return self.__right

    @property
    def txt(self) -> str:
        """
        :return: str, joined left, center and right contexts.
        """
        return f"{self.left} {self.center} {self.right}"

    @property
    def columns(self) -> List[str]:
        """ For csv writing.

        :return: list of str, names of columns.
        """
        return list(self.data.keys()) + ['URL']

    @property
    def items(self) -> List[str]:
        """ For csv writing, values of columns.

        :return: list of str or list, values of columns.
        """
        return list(self.data.values()) + [self.doc_url]

    @property
    def data(self) -> Dict:
        """
        :return: dict with fields names and their values.
        """
        data = {
            'left': self.left,
            'center': self.center,
            'right': self.right,
            'source': self.src,
            'found wordforms': ', '.join(self.found_wordforms)
        }
        return data

    @left.setter
    def left(self, other) -> None:
        """ Set left context.

        :param other: new left context.
        :return: None.
        """
        self.__left = other

    @center.setter
    def center(self, other) -> None:
        """ Set center context.

        :param other: new center context.
        :return: None.
        """
        self.__center = other

    @right.setter
    def right(self, other) -> None:
        """ Set right context.

        :param other: new right context.
        :return: None.
        """
        self.__right = other

    @txt.setter
    def txt(self, other) -> None:
        """ Exception, text setter not implemented to kwic """
        msg = "txt setter not implemented to kwic"
        logger.error(msg)
        raise NotImplementedError(msg)

    def mark_found_words(self,
                         marker: Callable) -> None:
        """ Mark found wordforms in all contexts using marker function.

        :param marker: function to mark found wordforms.
        :return: None.
        """
        self.__left = mark_found_words(self.left, self.found_wordforms, marker)
        self.__center = mark_found_words(self.center, self.found_wordforms, marker)
        self.__right = mark_found_words(self.right, self.found_wordforms, marker)

    def __str__(self) -> str:
        """ Str format:
                LEFT: example's left context.
                CENTER: example's center context.
                RIGHT: example's right context.
                SOURCE: example's source.
                FOUND WORDFORMS: example's found wordforms.

        :return: this str.
        """
        res = '\n'.join(
            f"{key.upper()}: {val}"
            for key, val in self.data.items()
        )
        return res

    def __repr__(self) -> str:
        """ Str format:
                    left: example's left context.
                    center: example's center context.
                    right: example's right context.
                    source: example's source.
                    found wordforms: example's found wordforms.
                    URL: example's URL.

        :return: this str.
        """
        res = '\n'.join(
            f"{key}: {val}"
            for key, val in self.data.items()
        )
        url = f"URL: {self.doc_url}"
        return f"{res}\n{url}"

    def __hash__(self) -> int:
        """ Hash str with all example fields.

        :return: int, hash.
        """
        return hash(repr(self))

    def __bool__(self) -> bool:
        """
        :return: bool, whether fields (expect for URL) exist.
        """
        return all(val for val in self.data.values())


class MainExample(Example):
    pass


class SyntaxExample(Example):
    pass


class Paper2000Example(Example):
    pass


class PaperRegionalExample(Example):
    pass


class ParallelExample(Example):
    def __init__(self,
                 txt: Dict[str, str],
                 src: str,
                 ambiguation: str,
                 found_wordforms: List[str],
                 doc_url: str) -> None:
        """
        :param txt: dict of str, {lang: text}
        :param src: str, examples source.
        :param ambiguation: str, examples ambiguation.
        :param found_wordforms: list of str, examples found wordforms.
        :param doc_url: str, examples URL.
        """
        super().__init__('', src, ambiguation, found_wordforms, doc_url)
        self.__txt = {lang: text for lang, text in txt.items()}

    @property
    def txt(self) -> Dict[str, str]:
        """ Get dict with all variants.

        :return: dict of str.
        """
        return self.__txt

    def mark_found_words(self,
                         marker: Callable) -> None:
        """ Mark found wordforms in the text with marker.

        :param marker: function to mark.
        :return: None.
        """
        for lang, txt in self.txt.items():
            self.__txt[lang] = mark_found_words(txt, self.found_wordforms, marker)

    # TODO: working with csv file
    # def items(self) -> List[str or list]:
    # def columns(self) -> List[str]:

    def __getattr__(self,
                    item: str) -> str or None:
        """ Get text in language.

        :param item: str, language.
        :return: str or None, text in the language if exists.
        """
        return self.txt.get(item, None)

    def __getitem__(self,
                    lang: str) -> str or None:
        """ Get text in language.

        :param item: str, language.
        :return: str or None, text in the language if exists.
        """
        return self.txt.get(lang, None)

    def __str__(self) -> str:
        """ Str format:
                LANG: text in the language
                SOURCE: examples source
                AMBIGUATION: examples ambiguation
                FOUND WORDFORMS: examples found wordforms

        :return: this str
        """
        data = self.txt
        data['source'] = self.src
        data['ambiguation'] = self.ambiguation
        data['found wordforms'] = ', '.join(self.found_wordforms)

        res = '\n'.join(
            f"{key.upper()}: {value}"
            for key, value in data.items()
        )
        return res


class TutoringExample(Example):
    pass


class DialectExample(Example):
    pass


class PoetryExample(Example):
    pass


class SpokenExample(Example):
    pass


class AccentologyExample(Example):
    pass


class MultimediaExample(Example):
    pass


class MultiparkExample(Example):
    pass


class HistoricalExample(Example):
    pass
