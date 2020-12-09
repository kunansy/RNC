__version__ = '0.5'

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
