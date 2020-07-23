__all__ = ('create_logger', 'create_formatter',
           'create_stream_handler', 'create_file_handler')
import logging

DEFAULT_MSG_FMT = "[{name}:{levelname}:{funcName}:{asctime}] {message}"
DEFAULT_DATE_FMT = "%d.%m.%Y %H:%M:%S"


def create_formatter(message_format: str = DEFAULT_MSG_FMT,
                     date_format: str = DEFAULT_DATE_FMT,
                     style: str = '{') -> logging.Formatter:
    """ Create message formatter.

    :param message_format: str, way to format message.
    :param date_format: str, way to format date.
     Str with %, because it need for time.strftime()
    :param style: str, % or {. Whether message_format
     contains % or { way to format.
    :return: logging.Formatter
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
     until the first logger calling.
    :keyword encoding: str, file encoding.
    :return: file handler.
    """
    file_handler = logging.FileHandler(log_path, **kwargs)
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
