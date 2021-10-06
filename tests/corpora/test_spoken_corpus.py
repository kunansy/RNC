from time import sleep

import rnc.corpora as rnc
from tests.corpora.template import TemplateCorpusTest


class TestSpokenCorpus(TemplateCorpusTest):
    corp_type = rnc.SpokenCorpus

    corp_normal_obj = corp_type('ты', 1, dpp=5, spd=1)
    corp_kwic_obj = corp_type('ты', 1, dpp=5, spd=1, out='kwic')

    corp_normal_obj.request_examples()
    sleep(5)
    corp_kwic_obj.request_examples()
    sleep(5)
