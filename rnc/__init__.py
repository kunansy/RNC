__version__ = '0.9.0'


import logging
import sys
from typing import Union

from .corpora import (
    MainCorpus,
    Paper2000Corpus,
    PaperRegionalCorpus,
    ParallelCorpus,
    DialectalCorpus,
    SpokenCorpus,
    AccentologicalCorpus,
    MultilingualParaCorpus,
    TutoringCorpus,
    MultimodalCorpus,

    SORT_KEYS,
    OUTPUT_FORMATS,
    SEARCH_FORMATS
)
from .corpora_params import Mycorp
from .examples import (
    MainExample,
    Paper2000Example,
    PaperRegionalExample,
    ParallelExample,
    DialectalExample,
    SpokenExample,
    AccentologicalExample,
    MultilingualParaExample,
    TutoringExample,
    MultimodalExample,
    KwicExample
)

MSG_FMT = "[{asctime},{msecs:3.0f}] [{levelname}] " \
          "[{module}:{funcName}] {message}"
DATE_FMT = "%d.%m.%Y %H:%M:%S"

LOGGER_NAME = "rnc"
LOG_FILE = f"{LOGGER_NAME}.log"


formatter = logging.Formatter(
    fmt=MSG_FMT, datefmt=DATE_FMT, style='{')

stream_handler = logging.StreamHandler()
stream_handler.setLevel(logging.WARNING)
stream_handler.setFormatter(formatter)

file_handler = logging.FileHandler(
    LOG_FILE, delay=True, encoding='utf-8')
file_handler.setLevel(logging.CRITICAL)
file_handler.setFormatter(formatter)

logger = logging.getLogger(LOGGER_NAME)
logger.setLevel(logging.DEBUG)

logger.addHandler(stream_handler)
logger.addHandler(file_handler)


def set_handler_level(handler_class: type):
    def wrapped(level: Union[int, str]) -> None:
        try:
            level = level.upper() # type: ignore
        except AttributeError:
            pass

        for handler in logger.handlers:
            if isinstance(handler, handler_class):
                handler.setLevel(level)
                return
        print(f"There is no '{handler_class}' handler."
              f"This behavior is undefined, contact the developer",
              file=sys.stderr)

    return wrapped


set_stream_handler_level = set_handler_level(logging.StreamHandler)
set_file_handler_level = set_handler_level(logging.FileHandler)


def set_logger_level(level: Union[int, str]) -> None:
    try:
        level = level.upper() # type: ignore
    except AttributeError:
        pass
    logger.setLevel(level)


mycorp = Mycorp()

__all__ = (
    'MainCorpus',
    'Paper2000Corpus',
    'PaperRegionalCorpus',
    'ParallelCorpus',
    'DialectalCorpus',
    'SpokenCorpus',
    'AccentologicalCorpus',
    'MultilingualParaCorpus',
    'TutoringCorpus',
    'MultimodalCorpus',
    'mycorp',

    'MainExample',
    'Paper2000Example',
    'PaperRegionalExample',
    'ParallelExample',
    'DialectalExample',
    'SpokenExample',
    'AccentologicalExample',
    'MultilingualParaExample',
    'TutoringExample',
    'MultimodalExample',
    'KwicExample',

    'set_stream_handler_level',
    'set_file_handler_level',
    'set_logger_level',

    'SORT_KEYS',
    'SEARCH_FORMATS',
    'OUTPUT_FORMATS'
)
