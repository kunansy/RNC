__version__ = '0.5'

import logging
import os
from pathlib import Path

DEFAULT_MSG_FMT = "[{name}:{module}:{levelname}:{funcName}:{asctime}] {message}"
DEFAULT_DATE_FMT = "%d.%m.%Y %H:%M:%S"

LOG_FOLDER = Path('logs')
os.makedirs(LOG_FOLDER, exist_ok=True)


def create_formatter(message_format: str = DEFAULT_MSG_FMT,
                     date_format: str = DEFAULT_DATE_FMT,
                     style: str = '{') -> logging.Formatter:
    """ Create message formatter.

    :param message_format: str, way to format message.
    :param date_format: str, way to format date.
     Str with %, because it is needed for time.strftime()
    :param style: str, % or {. Whether message_format
     contains % or { way to format.
    :return: logging.Formatter.
    """
    formatter = logging.Formatter(
        fmt=message_format,
        datefmt=date_format,
        style=style
    )
    return formatter


def create_stream_handler(level=logging.NOTSET,
                          formatter: logging.Formatter = None) -> logging.StreamHandler:
    """ Create stream handler.

    :param level: handler level. WARNING by default.
    :param formatter: Formatter, message format.
    :return: stream handler.
    """
    stream_handler = logging.StreamHandler()
    stream_handler.setLevel(level)
    formatter = formatter or create_formatter()
    stream_handler.setFormatter(formatter)

    return stream_handler


def create_file_handler(level=logging.DEBUG,
                        log_path: str = None,
                        formatter: logging.Formatter = None,
                        **kwargs) -> logging.FileHandler:
    """ Create file handler.

    :param level: handler level.
    :param log_path: str, path to log file.
    :param formatter: Formatter, message format.
    :keyword delay: bool, whether the file will not be opened
     until the first logger calling. True by default.
    :return: file handler.
    """
    delay = kwargs.pop('delay', True)

    file_handler = logging.FileHandler(
        log_path, delay=delay, encoding='utf-8', **kwargs)
    file_handler.setLevel(level)
    formatter = formatter or create_formatter()
    file_handler.setFormatter(formatter)

    return file_handler


def create_logger(module_name: str,
                  level=logging.DEBUG,
                  *handlers) -> logging.Logger:
    """ Create logger.

    :param module_name: str, name of logger.
    :param level: level of logger, DEBUG by default.
    :param handlers: handlers to be added to the logger.
    :return: logger.
    """
    logger_ = logging.getLogger(module_name)
    logger_.setLevel(level)

    path = LOG_FOLDER / f"{module_name}.log"

    handlers = handlers or [
        create_stream_handler(),
        create_file_handler(log_path=path)
    ]

    for handler in handlers:
        logger_.addHandler(handler)

    return logger_


logger = create_logger("rnc")

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
    MultimodalCorpus
)
from .corpora_params import Subcorpus
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


def set_stream_handlers_level(level) -> None:
    import rnc.corpora_requests

    # TODO:
    examples.logger[0].setLevel(level)
    corpora.logger[0].setLevel(level)
    corpora_requests.logger[0].setLevel(level)


subcorpus = Subcorpus()

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
    'subcorpus',

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

    'set_stream_handlers_level'
)
