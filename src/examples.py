__all__ = (
    'MainExample', 'SyntaxExample', 'PaperExample', 'ParallelExample',
    'TutoringExample', 'DialectExample', 'PoetryExample', 'SpeechExample',
    'AccentologyExample', 'MultimediaExample', 'MultiparkExample',
    'HistoricalExample', 'KwicExample'
)

import logging
import re
import webbrowser
from pathlib import Path
from typing import List, Callable, Dict

import src.corpora_logging as clog

log_folder = Path("logs")
log_file = log_folder / f"{__name__}.log"

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


def mark_found_words(txt: str,
                     found_wordforms: List[str],
                     marker: Callable) -> str:
    if marker is None:
        return txt
    # TODO: correct it
    for word in found_wordforms:
        repls = re.findall(
            fr'(\W+{word}\W+)|(^{word}\W+)|(\W+{word}$)|(^{word}$)', txt)
        for group in repls:
            for num, i in enumerate(group, 1):
                if num is 3 and i:
                    txt = f"{txt[:txt.rindex(i)]}{marker(i)}"
                elif num is not 3:
                    txt = txt.replace(i, marker(i), 1)
    return txt
    # проблемный вариант, '. {w}' может встретиться не в конце
    # "я Решения, . яма я такое: ,я,готовится . я"
    # re.findall(r'(\W+я\W+)|(^я\W+)|(\W+я$)|(^я$)', string)


class Example:
    """ Base examples class """
    __slots__ = (
        '__txt', '__src', '__doc_url',
        '__ambiguation', '__found_wordforms')

    def __init__(self,
                 txt: str,
                 src: str,
                 ambiguation: str,
                 found_wordforms: List[str],
                 doc_url: str) -> None:
        """
        :param txt: str, the text in example.
        :param src: str, example source.
        :param ambiguation: str, whether the example disambiguated.
        :param found_wordforms: list of str, for these words request was.
        :param doc_url: str, url to the doc.
        :return: None.
        """
        self.__txt = txt
        self.__src = src
        self.__ambiguation = ambiguation
        self.__found_wordforms = found_wordforms or []
        self.__doc_url = doc_url

    @property
    def txt(self) -> str:
        """
        :return: str, text in the example.
        """
        return self.__txt

    @property
    def src(self) -> str:
        """
        :return: str, source of the example.
        """
        return self.__src

    @property
    def ambiguation(self) -> str:
        """
        :return: str, ambiguation in the example.
        """
        return self.__ambiguation

    @property
    def doc_url(self) -> str:
        """
        :return: str, URL of the example.
        """
        return self.__doc_url

    @property
    def found_wordforms(self) -> List[str]:
        """
        :return: list of str, found wordforms in the example.
        """
        return self.__found_wordforms

    @property
    def columns(self) -> List[str]:
        """ For csv writing, names of columns.

        :return: list of str, names of columns.
        """
        return ['text', 'source', 'ambiguation',
                'found_wordforms', 'URL']

    @property
    def items(self) -> List[str or list]:
        """ For csv writing, values of columns.

        :return: list of str or list, values of columns.
        """
        # ATTENTION: these values order must
        # be the same as in constructor
        return [self.txt, self.src, self.ambiguation,
                self.found_wordforms, self.doc_url]

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
        except Exception as e:
            logger.exception(
                f"Error while opening doc with url: {self.doc_url}")
            raise e

    def mark_found_words(self,
                         marker: Callable) -> None:
        """ Mark found wordforms in the text with marker.

        :param marker: function to mark found wordforms.
        :return: None.
        """
        self.__txt = mark_found_words(self.txt, self.found_wordforms, marker)

    def __str__(self) -> str:
        """ Str format:
                    TEXT: examples text
                    SOURCE: examples source
                    AMBIGUATION: examples ambiguation
                    FOUND WORDFORMS: examples found wordforms

        :return: this str.
        """
        data = {
            'text': self.txt,
            'source': self.src,
            'ambiguation': self.ambiguation,
            'found wordforms': ', '.join(self.found_wordforms)
        }
        res = '\n'.join(
            f"{key.upper()}: {val}"
            for key, val in data.items()
        )
        return res

    def __repr__(self) -> str:
        """ Str format:
                Text: ...
                Source: ...
                Ambiguation: ...
                Found wordforms: ...
                URL: ...

        :return: this str.
        """
        res = f"Text: {self.txt}\n" \
              f"Source: {self.src}\n" \
              f"Found wordforms: {self.found_wordforms}\n" \
              f"Ambiguation: {self.ambiguation}\n" \
              f"URL: {self.doc_url}"
        return res

    def __hash__(self) -> int:
        """ Hash str with all example fields.

        :return: int, hash.
        """
        data = f"{self.txt}{self.src}{self.ambiguation}" \
               f"{self.found_wordforms}{self.doc_url}"
        return hash(data)

    def __bool__(self) -> bool:
        """ Whether fields (expect for found_wordforms) exist.

        :return: bool.
        """
        return bool(self.txt and self.src and
                    self.doc_url and self.ambiguation)


class KwicExample(Example):
    def __init__(self,
                 left: str,
                 center: str,
                 right: str,
                 src: str,
                 found_wordforms: List[str],
                 doc_url: str) -> None:
        """ There's no ambiguation, it set with ''."""
        self.__left = left
        self.__center = center
        self.__right = right
        super().__init__(self.txt, src, '', found_wordforms, doc_url)

    @property
    def left(self) -> str:
        """
        :return: str, left context.
        """
        return self.__left

    @property
    def center(self) -> str:
        """
        :return: str, center context.
        """
        return self.__center

    @property
    def right(self) -> str:
        """
        :return: str, right context.
        """
        return self.__right

    @property
    def txt(self) -> str:
        """
        :return: str, joined left, center and right contexts
        with removed duplicate spaces.
        """
        txt = f"{self.left} {self.center} {self.right}"
        return ' '.join(txt.split())

    @property
    def columns(self) -> List[str]:
        """ For csv writing, names of columns.

        :return: list of str, names of columns.
        """
        return ['left', 'center', 'right', 'source', 'found_wordforms', 'URL']

    @property
    def items(self) -> List[str]:
        """ For csv writing, values of columns.

        :return: list of str or list, values of columns.
        """
        return [self.left, self.center, self.right,
                self.src, self.found_wordforms, self.doc_url]

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
                LEFT: examples left context.
                CENTER: examples center context.
                RIGHT: examples right context.
                SOURCE: examples source.
                FOUND WORDFORMS: examples found wordforms.

        :return: this str.
        """
        data = {
            'left': self.left,
            'center': self.center,
            'right': self.right,
            'source': self.src,
            'found wordforms': ', '.join(self.found_wordforms)
        }
        res = '\n'.join(
            f"{key.upper()}: {val}"
            for key, val in data.items()
        )
        return res

    def __hash__(self) -> int:
        """ Hash str with all example fields.

        :return: int, hash.
        """
        data = f"{self.left}{self.center}{self.right}{self.src}{self.doc_url}"
        return hash(data)

    def __bool__(self) -> bool:
        """ Whether fields (expect for found_wordforms) exist.

        :return: bool.
        """
        txt = self.left and self.center and self.right
        metadata = self.src and self.doc_url
        return bool(txt and metadata)


class MainExample(Example):
    pass


class SyntaxExample(Example):
    pass


class PaperExample(Example):
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


class SpeechExample(Example):
    pass


class AccentologyExample(Example):
    pass


class MultimediaExample(Example):
    pass


class MultiparkExample(Example):
    pass


class HistoricalExample(Example):
    pass
