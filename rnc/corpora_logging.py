__all__ = (
    'create_logger', 'create_formatter', 'log_folder',
    'create_file_handler', 'create_stream_handler')

import logging
import os
from pathlib import Path

DEFAULT_MSG_FMT = "[{name}:{levelname}:{funcName}:{asctime}] {message}"
DEFAULT_DATE_FMT = "%d.%m.%Y %H:%M:%S"


def create_folder(folder_name: str = 'logs') -> Path:
    """ Create folder named 'logs' and return path to it.

    :param folder_name: str, name of folder.
    :return: None.
    """
    folder_path = Path(folder_name)
    if folder_path.exists():
        return folder_path

    os.mkdir(folder_path)
    return folder_path


def create_formatter(message_format: str = DEFAULT_MSG_FMT,
                     date_format: str = DEFAULT_DATE_FMT,
                     style: str = '{') -> logging.Formatter:
    """ Create message formatter.

    :param message_format: str, way to format message.
    :param date_format: str, way to format date.
     Str with %, because it needed for time.strftime()
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


def create_stream_handler(level=logging.WARNING,
                          formatter=None) -> logging.Handler:
    """ Create stream handler.

    :param level: handler level. WARNING by default.
    :param formatter: message formatter. None by default.
    :return: stream handler.
    """
    stream_handler = logging.StreamHandler()
    stream_handler.setLevel(level)
    if formatter:
        stream_handler.setFormatter(formatter)

    return stream_handler


def create_file_handler(level=logging.DEBUG,
                        log_path: str = None,
                        formatter=None,
                        **kwargs) -> logging.StreamHandler:
    """ Create file handler.

    :param level: handler level.
    :param log_path: str, log file path.
    :param formatter: message formatter.
    :param kwargs: params to FileHandler constructor.
    :keyword delay: bool, whether file'll not be opened
     until the first logger calling. True by default.
    :keyword encoding: str, file encoding. utf-8 by default.
    :return: file handler.
    """
    delay = kwargs.pop('delay', True)
    encoding = kwargs.pop('encoding', 'utf-8')

    file_handler = logging.FileHandler(
        log_path, delay=delay, encoding=encoding, **kwargs)
    file_handler.setLevel(level)
    if formatter:
        file_handler.setFormatter(formatter)

    return file_handler


def create_logger(name: str,
                  level=logging.DEBUG,
                  *handlers) -> logging.Logger:
    """ Create logger.

    :param name: str, name of logger.
    :param level: level of logger.
    :param handlers: handlers to be added to the logger.
    :return: logger.
    """
    logger = logging.getLogger(name)
    logger.setLevel(level)

    for handler in handlers:
        logger.addHandler(handler)

    return logger


log_folder = create_folder()