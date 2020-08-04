__version__ = '0.3.1'

from .corpora import MainCorpus

from .corpora import Subcorpus
from .examples import MainExample
from .examples import KwicExample


def set_stream_handlers_level(level) -> None:
    import rnc.corpora_requests

    examples.stream_handler.setLevel(level)
    corpora.stream_handler.setLevel(level)
    corpora_requests.stream_handler.setLevel(level)


def set_file_handlers_level(level) -> None:
    import rnc.corpora_requests

    examples.file_handler.setLevel(level)
    corpora.file_handler.setLevel(level)
    corpora_requests.file_handler.setLevel(level)


def set_loggers_level(level) -> None:
    import rnc.corpora_requests

    examples.logger.setLevel(level)
    corpora.logger.setLevel(level)
    corpora_requests.logger.setLevel(level)


__all__ = (
    'MainCorpus',
    'Subcorpus',
    'MainExample',
    'KwicExample',
    'set_loggers_level',
    'set_file_handlers_level',
    'set_stream_handlers_level'
)

