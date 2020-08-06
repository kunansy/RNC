__version__ = '0.3.2'

from .corpora import (
    Subcorpus,
    MainCorpus,
    Paper2000Corpus,
    PaperRegionalCorpus,
    ParallelCorpus,
    DialectCorpus,
    SpokenCorpus,
    AccentologyCorpus
)
from .examples import (
    MainExample,
    Paper2000Example,
    PaperRegionalExample,
    ParallelExample,
    DialectExample,
    SpokenExample,
    AccentologyExample,
    KwicExample
)


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
    'Paper2000Corpus',
    'PaperRegionalCorpus',
    'ParallelCorpus',
    'DialectCorpus',
    'SpokenCorpus',
    'AccentologyCorpus',
    'Subcorpus',

    'MainExample',
    'Paper2000Example',
    'PaperRegionalExample',
    'ParallelExample',
    'DialectExample',
    'SpokenExample',
    'AccentologyExample',
    'KwicExample',

    'set_loggers_level',
    'set_file_handlers_level',
    'set_stream_handlers_level'
)
