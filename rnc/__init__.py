__version__ = '0.2'

from .corpora import MainCorpus

from .corpora import Subcorpus
from .examples import MainExample
from .examples import KwicExample

__all__ = (
    'MainCorpus',
    'Subcorpus',
    'MainExample',
    'KwicExample'
)

