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
from typing import List, Callable, Dict, Any

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
        '_txt', '_src', '_doc_url',
        '_ambiguation', '_found_wordforms')

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
        self._txt = txt
        self._src = src
        self._ambiguation = ambiguation
        self._doc_url = doc_url

        wf = found_wordforms or []
        if isinstance(wf, str):
            wf = found_wordforms.split(', ')
        self._found_wordforms = wf

    @property
    def txt(self) -> str:
        """
        :return: str, example's text.
        """
        return self._txt

    @property
    def src(self) -> str:
        """
        :return: str, example's source.
        """
        return self._src

    @property
    def ambiguation(self) -> str:
        """
        :return: str, example's ambiguation.
        """
        return self._ambiguation

    @property
    def doc_url(self) -> str:
        """
        :return: str, example's URL.
        """
        return self._doc_url

    @property
    def found_wordforms(self) -> List[str]:
        """
        :return: list of str, example's found wordforms.
        """
        return self._found_wordforms

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
        """ There're all fields except for doc_url.
        Found wordforms joined with ', '.

        :return: dict with fields names and their values.
        """
        data = {
            'text': self._txt,
            'source': self._src,
            'ambiguation': self._ambiguation,
            'found wordforms': ', '.join(self._found_wordforms)
        }
        return data

    @txt.setter
    def txt(self, other) -> None:
        """ Set text.

        :return: None.
        """
        self._txt = other

    @ambiguation.setter
    def ambiguation(self, other) -> None:
        """ Set ambiguation.

        :return: None.
        """
        self._ambiguation = other

    def open_doc(self) -> None:
        """ Open the doc in the new tab of the default browser.

        :return: None.
        :exception ValueError: URL is not like 'http...'
        :exception: if something's wrong.
        """
        if not self._doc_url.startswith('http'):
            logger.exception(
                f"Tried to open doc with wrong url: {self._doc_url}")
            raise ValueError(f"Wrong URL: {self._doc_url}")
        try:
            webbrowser.open_new_tab(self._doc_url)
        except Exception:
            logger.exception(
                f"Error while opening doc with url: {self._doc_url}")
            raise

    def mark_found_words(self,
                         marker: Callable) -> None:
        """ Mark found wordforms in the text with marker.

        :param marker: function to mark found wordforms.
        :return: None.
        """
        self._txt = mark_found_words(
            self._txt, self._found_wordforms, marker)

    def __copy__(self):
        """
        :return: copied obj.
        """
        return self.__class__(*self.data.values(), self.doc_url)

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
        """ Text setter not implemented to kwic """
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
                 txt: Dict[str, str] = None,
                 src: str = '',
                 ambiguation: str = '',
                 found_wordforms: List[str] = None,
                 doc_url: str = '') -> None:
        """
        :param txt: dict of str, {lang: text}
        :param src: str, examples source.
        :param ambiguation: str, examples ambiguation.
        :param found_wordforms: list of str, examples found wordforms.
        :param doc_url: str, examples URL.
        """
        txt = txt or {}
        found_wordforms = found_wordforms or []

        super().__init__(txt, src, ambiguation, found_wordforms, doc_url)

    @property
    def txt(self) -> Dict[str, str]:
        """ Get dict with all variants.

        :return: dict of str.
        """
        return self._txt

    @txt.setter
    def txt(self, other: Any) -> None:
        """ Text setter not implemented to the ParallelExample """
        msg = "Try to use ex['lang'] instead"
        logger.error(msg)
        raise NotImplementedError(msg)

    @property
    def data(self) -> Dict:
        """ There're all fields except for doc_url.
        Found wordforms joined with ', '.

        :return: dict with fields names and their values.
        """
        data = self.txt.copy()
        data['source'] = self.src
        data['ambiguation'] = self.ambiguation
        data['found wordforms'] = ', '.join(self.found_wordforms)

        return data

    def mark_found_words(self,
                         marker: Callable) -> None:
        """ Mark found wordforms in the text with marker.

        :param marker: function to mark.
        :return: None.
        """
        for lang, txt in self.txt.items():
            self[lang] = mark_found_words(
                txt, self.found_wordforms, marker)

    @staticmethod
    def _best_src(f_src: str,
                  s_src: str) -> str:
        """ Choose the best source, means there're
        two translations in it.

        :param f_src: str, first source.
        :param s_src: str, second source.
        :return: str, best of them.
        """
        if '|' in s_src:
            return s_src
        return f_src

    def __copy__(self) -> Any:
        """
        :return: copied obj.
        """
        obj = super().__copy__()
        obj._txt = self.txt.copy()
        return obj

    def __iadd__(self, other) -> Any:
        """ Concatenate two examples:
            – join the texts

            – choose the best source, there're
            two translations there

            – choose where the text is disambiguated.

            – join found wordforms.

        :param other: instance of the same class.
        :return: self.
        :exception TypeError: if wrong type given.
        """
        if not isinstance(other, self.__class__):
            msg = f"'+=' supported only {self.__class__} objects"
            logger.error(msg)
            raise TypeError(msg)

        for lang, txt in other.txt.items():
            if lang in self.txt:
                self[lang] = f"{self.txt[lang]} {txt}"
            else:
                self[lang] = txt

        # source contains two translations
        self._src = ParallelExample._best_src(self.src, other.src)

        if not (self.ambiguation and 'not' in other.ambiguation):
            self._ambiguation = other.ambiguation
        if not self.doc_url:
            self._doc_url = other.doc_url
        self._found_wordforms += other.found_wordforms

        return self

    def __getattr__(self,
                    item: str) -> str or None:
        """ Get text in language.

        :param item: str, language.
        :return: str or None, text in the language if exists.
        """
        return self.txt.get(item, None)

    def __getitem__(self,
                    lang: str) -> str or None:
        """ Get text in the language.

        :param lang: str, language.
        :return: str or None, text in the language if exists.
        """
        return self.lang

    def __setitem__(self,
                    lang: str,
                    txt: str) -> None:
        """ Change text in the lang.

        :param lang: str, lang tag.
        :param txt: str, new text.
        :return: None.
        :exception ValueError: if the text in the lang doesn't exist.
        """
        self._txt[lang] = txt


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
