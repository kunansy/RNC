__version__ = '0.6.4.1'


import logging
import os
from pathlib import Path
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

MSG_FMT = "[{levelname}:{module}:{funcName}:{lineno} line:" \
          "{asctime},{msecs:.0f}] {message}"
DATE_FMT = "%d.%m.%Y %H:%M:%S"

LOGGER_NAME = "rnc"
LOG_FOLDER = Path('logs')
LOG_FILE = LOG_FOLDER / f"{LOGGER_NAME}.log"
os.makedirs(LOG_FOLDER, exist_ok=True)

LEVEL = Union[str, int]


formatter = logging.Formatter(
    fmt=MSG_FMT, datefmt=DATE_FMT, style='{')

stream_handler = logging.StreamHandler()
stream_handler.setLevel(logging.WARNING)
stream_handler.setFormatter(formatter)

file_handler = logging.FileHandler(
    LOG_FILE, delay=True, encoding='utf-8')
file_handler.setLevel(logging.DEBUG)
file_handler.setFormatter(formatter)

logger = logging.getLogger(LOGGER_NAME)
logger.setLevel(logging.DEBUG)

logger.addHandler(stream_handler)
logger.addHandler(file_handler)


class HandlerNotExistError(Exception):
    pass


def set_handler_level(level: LEVEL,
                      handler_class: type) -> None:
    try:
        level = level.upper()
    except AttributeError:
        pass
 
    for handler_index in range(len(logger.handlers)):
        if logger.handlers[handler_index].__class__ == handler_class:
            logger.handlers[handler_index].setLevel(level)
            return
    raise HandlerNotExistError(f"There is no '{handler_class}' handler")


def set_stream_handler_level(level: LEVEL) -> None:
    try:
        set_handler_level(level, logging.StreamHandler)
    except HandlerNotExistError:
        print("Stream handler doesn't exist. This behavior "
              "is undefined, contact the developer")


def set_file_handler_level(level: LEVEL) -> None:
    try:
        set_handler_level(level, logging.FileHandler)
    except HandlerNotExistError:
        print("File handler doesn't exist. This behavior "
              "is undefined, contact the developer")


def set_logger_level(level: LEVEL) -> None:
    try:
        level = level.upper()
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
