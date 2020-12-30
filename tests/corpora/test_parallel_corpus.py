from time import sleep

import rnc.corpora as rnc
from tests.corpora.template import TemplateCorpusTest


class TestParallelCorpus(TemplateCorpusTest):
    corp_type = rnc.ParallelCorpus

    corp_normal_obj = corp_type('ты', 1, dpp=5, spd=1)
    corp_kwic_obj = corp_type('ты', 1, dpp=5, spd=1, out='kwic')

    corp_normal_obj.request_examples()
    sleep(5)
    corp_kwic_obj.request_examples()
    sleep(5)

    def test_full_query_with_lexform(self):
        corp = self.corp_type('Владимир Путин', 1, text='lexform')
        corp.request_examples()

        assert len(corp) > 1
        sleep(5)

    def test_mycorp(self):
        corp = self.corp_type(
            'ты', 1,
            mycorp='JSONeyJkb2NfaV9sZV9zdGFydF95ZWFyIjogWyIyMDAwIl19'
        )
        corp.request_examples()

        assert len(corp) >= 1
        sleep(5)

    def test_sort_data(self):
        copy = self.corp_normal_obj.copy()
        copy.sort_data(key=lambda x: len(x.ru))

        assert copy.data != self.corp_normal_obj.data
