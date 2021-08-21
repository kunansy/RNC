__all__ = (
    'MainExample',
    'SyntaxExample',
    'Paper2000Example',
    'PaperRegionalExample',
    'ParallelExample',
    'MultilingualParaExample',
    'TutoringExample',
    'DialectalExample',
    'PoeticExample',
    'SpokenExample',
    'AccentologicalExample',
    'MultimodalExample',
    'MultiPARCExample',
    'HistoricalExample',
    'TutoringExample',
    'KwicExample'
)

import logging
import os
import re
import webbrowser
from pathlib import Path
from typing import List, Callable, Dict, Any

import rnc.corpora_requests as creq

logger = logging.getLogger("rnc")


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
        :param found_wordforms: list of str, None or str joined with ', ',
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
    def txt(self) -> Any:
        """
        :return: any type, example's text.
        """
        return self._txt

    @property
    def src(self) -> Any:
        """
        :return: any type, example's source.
        """
        return self._src

    @property
    def ambiguation(self) -> Any:
        """
        :return: any type, example's ambiguation.
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
    def items(self) -> List[Any]:
        """ For csv writing.

        :return: list of any types, values of columns.
        """
        # ATTENTION:
        # these order must be the same as in the constructor
        return list(self.data.values()) + [self.doc_url]

    @property
    def data(self) -> Dict[str, Any]:
        """ There are all fields except for doc_url.
        Found wordforms joined with ', '.

        :return: dict with fields names and their values.
        """
        data = {
            'text': self.txt,
            'source': self.src,
            'ambiguation': self.ambiguation,
            'found wordforms': ', '.join(self.found_wordforms)
        }
        return data

    @txt.setter
    def txt(self,
            other: Any) -> None:
        """ Set text.

        :param other: any type, new txt.
        :return: None.
        """
        if not isinstance(other, str):
            class_name = self.__class__.__name__
            logger.warning(f"As a text to {class_name} "
                           f"set {type(other)}, str expected")

        self._txt = other

    @src.setter
    def src(self,
            other: Any) -> None:
        """ Set source.

        :param other: any type, new src.
        :return: None.
        """
        if not isinstance(other, str):
            class_name = self.__class__.__name__
            logger.warning(f"As a source to {class_name} "
                           f"set {type(other)}, str expected")

        self._src = other

    @ambiguation.setter
    def ambiguation(self,
                    other: Any) -> None:
        """ Set ambiguation.

        :param other: any type, new ambiguation.
        :return: None.
        """
        if not isinstance(other, str):
            class_name = self.__class__.__name__
            logger.warning(f"As a ambiguation to {class_name} "
                           f"set {type(other)}, str expected")
        self._ambiguation = other

    def open_doc(self) -> None:
        """ Open the doc in the new tab of the default browser.

        :return: None.
        :exception: if something is wrong.
        """
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
            self.txt, self.found_wordforms, marker)

    def copy(self) -> Any:
        """
        :return: copied obj.
        """
        return self.__class__(*self.data.values(), self.doc_url)

    def __eq__(self,
               other: Any) -> bool:
        """ ==

        :param other: other Example object.
        :return: bool, whether data equal.
        """
        return self.items == other.items

    def __contains__(self,
                     item: Any) -> bool:
        """ Whether the item is in the text.
        Registers equaled (if it is available).

        :param item: any type, item to check.
        :return: whether item is in text.
        """
        try:
            return item.lower() in self.txt.lower()
        except AttributeError:
            return item in self.txt

    def __str__(self) -> str:
        """ Str format:
            TEXT: ...
            SOURCE: ...
            AMBIGUATION: ...
            FOUND WORDFORMS: ...

        :return: this str.
        """
        res = '\n'.join(
            f"{key.upper()}: {val}"
            for key, val in self.data.items()
        )
        return res

    def __repr__(self) -> str:
        """ Str format:
            text: ...
            source: ...
            ambiguation: ...
            found wordforms: ...
            URL: ...

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
    __slots__ = '_left', '_center', '_right'

    def __init__(self,
                 left: str,
                 center: str,
                 right: str,
                 src: str,
                 found_wordforms: List[str] or str,
                 doc_url: str) -> None:
        """ There is no ambiguation, it set with ''.

        :param left: str, example's left context.
        :param center: str, example's center context.
        :param right: str, example's right context.
        :param src: str, example's source.
        :param found_wordforms: list of str or str, example's found wordforms.
        :param doc_url: str, example's URL.
        """
        self._left = left
        self._center = center
        self._right = right
        super().__init__(self.txt, src, '', found_wordforms, doc_url)

    @property
    def left(self) -> Any:
        """
        :return: str, example's left context.
        """
        return self._left

    @property
    def center(self) -> Any:
        """
        :return: str, example's center context.
        """
        return self._center

    @property
    def right(self) -> Any:
        """
        :return: str, example's right context.
        """
        return self._right

    @property
    def txt(self) -> str:
        """
        :return: str, joined left, center and right contexts.
        """
        # it's assumed that all contexts are stripped
        return f"{self.left} {self.center} {self.right}"

    @property
    def ambiguation(self) -> None:
        msg = "There is no ambiguation in KWICExamples"
        logger.error(msg)
        raise NotImplementedError(msg)

    @property
    def data(self) -> Dict[str, Any]:
        """ All fields except for URL.

        :return: dict with fields' names and their values.
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
    def left(self,
             other: Any) -> None:
        """ Set left context.

        :param other: any type, new left context.
        :return: None.
        """
        if not isinstance(other, str):
            class_name = self.__class__.__name__
            logger.warning(f"As a left context to {class_name} "
                           f"set {type(other)}, str expected")
        self._left = other

    @center.setter
    def center(self,
               other: Any) -> None:
        """ Set center context.

        :param other: any type, new center context.
        :return: None.
        """
        if not isinstance(other, str):
            class_name = self.__class__.__name__
            logger.warning(f"As a center context to {class_name} "
                           f"set {type(other)}, str expected")
        self._center = other

    @right.setter
    def right(self,
              other: Any) -> None:
        """ Set right context.

        :param other: any type, new right context.
        :return: None.
        """
        if not isinstance(other, str):
            class_name = self.__class__.__name__
            logger.warning(f"As a right context to {class_name} "
                           f"set {type(other)}, str expected")
        self._right = other

    @txt.setter
    def txt(self,
            other: Any) -> None:
        """ Text setter not implemented to KWICExamples """
        msg = "Text setter not implemented to KWICExamples"
        logger.error(msg)
        raise NotImplementedError(msg)

    def mark_found_words(self,
                         marker: Callable) -> None:
        """ Mark found wordforms in all contexts using marker.

        :param marker: function to mark found wordforms.
        :return: None.
        """
        words = self.found_wordforms
        self._left = mark_found_words(self.left, words, marker)
        self._center = mark_found_words(self.center, words, marker)
        self._right = mark_found_words(self.right, words, marker)


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
                 found_wordforms: List[str] or str = None,
                 doc_url: str = '') -> None:
        """
        :param txt: dict of str, {language tag: text}
        :param src: str, examples source.
        :param ambiguation: str, examples ambiguation.
        :param found_wordforms: list of str, examples found wordforms.
        :param doc_url: str, examples URL.
        """
        txt = txt or {}

        super().__init__(txt, src, ambiguation, found_wordforms, doc_url)
        self.sort()

    @property
    def txt(self) -> Dict[str, Any]:
        """ Get dict with texts.

        :return: dict of any types.
        """
        return self._txt

    @txt.setter
    def txt(self,
            other: Any) -> None:
        """ Text setter not implemented to the ParallelExample """
        msg = ("Text setter not implemented to ParallelExamples. "
               "Try to use ex['language tag'] instead")
        logger.error(msg)
        raise NotImplementedError(msg)

    @property
    def data(self) -> Dict[str, Any]:
        """ There are all fields except for doc_url.
        Found wordforms joined with ', '.

        :return: dict with fields' names and their values.
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
        """ Choose the best source, means
        there are two translations in it.

        :param f_src: str, first source.
        :param s_src: str, second source.
        :return: str, best of them.
        """
        if '|' in s_src:
            return s_src
        return f_src

    def sort(self,
             key: Callable = None,
             reverse: bool = False) -> None:
        """ Sort txt dict, allowing the key to
        items() from there.

        :param key: callable, key to sort. Sort by language tag by default.
        :param reverse: bool, whether sorting will be in reversed order.
        :return: None.
        """
        key = key or (lambda items: items[0])
        data = sorted(self.txt.items(), key=key, reverse=reverse)
        self._txt = dict(data)

    def copy(self) -> Any:
        """
        :return: copied obj.
        """
        txt_copy = self.txt.copy()
        return self.__class__(
            txt_copy, self.src, self.ambiguation,
            self.found_wordforms, self.doc_url
        )

    def __contains__(self,
                     item: Any) -> bool:
        """ Whether the item is in the text.
        Registers equaled (if it is available).

        :param item: any type, item to check.
        :return: whether item is in text.
        """
        try:
            return any(item.lower() in i.lower() for i in self.txt.values())
        except AttributeError:
            return any(item in i for i in self.txt.values())

    def __iadd__(self,
                 other: Any) -> Any:
        """ Concatenate two examples:
            – join the texts

            – choose the best source, there are
            two translations there

            – choose where the text is disambiguated.

            – join found wordforms.

        :param other: instance of the same class.
        :return: self.
        :exception TypeError: if wrong type given.
        """
        if not isinstance(other, self.__class__):
            class_name = self.__class__.__name__
            msg = (f"'+=' supported only with '{class_name}' "
                   f"objects, but {type(other)} given")
            logger.error(msg)
            raise TypeError(msg)

        for lang, txt in other.txt.items():
            new_txt = f"{self.txt.get(lang, '')} {txt}"
            self[lang] = new_txt.lstrip()
        # save the order of languages
        self.sort(lambda x: x[0])
        # source contains two translations
        self._src = self.__class__._best_src(self.src, other.src)

        # for MultilingualParaCorpus
        if not self.src:
            self._src = other.src

        o_amb = other.ambiguation
        if not self.ambiguation or o_amb and 'not' not in o_amb:
            self._ambiguation = o_amb
        if not self.doc_url:
            self._doc_url = other.doc_url
        self._found_wordforms += other.found_wordforms

        return self

    def __getattr__(self,
                    item: str) -> Any:
        """ Get the text in language.

        :param item: str, language tag.
        :return: str or None, text in the language if exists.
        """
        try:
            return getattr(super(), item)
        except AttributeError:
            return self.txt.get(item, None)

    def __getitem__(self,
                    lang: str) -> Any:
        """ Get text in the language.

        :param lang: str, language tag.
        :return: str or None, text in the language if exists.
        """
        return self.txt.get(lang, None)

    def __setitem__(self,
                    lang: str,
                    txt: Any) -> None:
        """ Change text in the language.

        :param lang: str, language tag.
        :param txt: any type, new text.
        :return: None.
        :exception ValueError: if the text in the language does not exist.
        """
        if not isinstance(txt, str):
            class_name = self.__class__.__name__
            logger.warning(f"As a '{lang}' to {class_name} "
                           f"set {type(txt)}, str expected")
        self._txt[lang] = txt


class MultilingualParaExample(ParallelExample):
    pass


class TutoringExample(Example):
    pass


class DialectalExample(Example):
    pass


class PoeticExample(Example):
    pass


class SpokenExample(Example):
    pass


class AccentologicalExample(Example):
    pass


class MultimodalExample(Example):
    def __init__(self,
                 txt: str,
                 src: str,
                 ambiguation: str,
                 found_wordforms: List[str] or str,
                 doc_url: str,
                 media_url: str,
                 filename: str) -> None:
        """
        :param txt: str, example's text.
        :param src: str, example's source.
        :param ambiguation: str, example's ambiguation.
        :param found_wordforms: list of str, None or str joined with ', ',
        example's found wordforms.
        :param doc_url: str, example's url.
        :param media_url: str, URL to example's media file.
        :param filename: str or Path, default name of the file (from RNC).
        :return: None.
        """
        super().__init__(txt, src, ambiguation, found_wordforms, doc_url)
        self._media_url = media_url
        self._filepath = Path(filename)

    @property
    def filepath(self) -> Path:
        """ Get the path to the local file.

        :return: Path to the file.
        """
        return self._filepath

    @filepath.setter
    def filepath(self,
                 other: str or Path) -> None:
        """ Set new path to the local file.

        ATTENTION: if the file exists it will not be moved to
        the new path. You should call 'download_file()' again.

        :param other: str or Path, new path to the local file.
        :return: None.
        """
        self._filepath = Path(other)

    @property
    def columns(self) -> List[str]:
        """ For csv writing.

        :return: list of str, names of columns.
        """
        return super().columns + ['media_url', 'filename']

    @property
    def items(self) -> List[Any]:
        """ For csv writing.

        :return: list of any types, values of columns.
        """
        return super().items + [self._media_url, self.filepath]

    def download_file(self) -> None:
        """ Download the media file.

        :return: None.
        """
        os.makedirs(self.filepath.parent, exist_ok=True)

        data = [(self._media_url, str(self.filepath))]
        try:
            creq.download_docs(data)
        except Exception as e:
            logger.error(str(e))
            raise

    async def download_file_async(self) -> None:
        os.makedirs(self.filepath.parent, exist_ok=True)

        data = [(self._media_url, str(self.filepath))]
        try:
            await creq.download_docs_async(data)
        except Exception as e:
            logger.error(str(e))
            raise

    def copy(self) -> Any:
        return self.__class__(
            *self.data.values(), self.doc_url,
            self._media_url, str(self.filepath)
        )


class MultiPARCExample(Example):
    pass


class HistoricalExample(Example):
    pass
