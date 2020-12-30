from time import sleep

import pytest

import rnc.corpora as rnc
from tests.corpora.template import TemplateCorpusTest


class TestDialectalCorpus(TemplateCorpusTest):
    corp_type = rnc.DialectalCorpus

    corp_normal_obj = corp_type('ты', 1, dpp=5, spd=1)
    corp_kwic_obj = corp_type('ты', 1, dpp=5, spd=1, out='kwic')

    corp_normal_obj.request_examples()
    sleep(5)
    corp_kwic_obj.request_examples()
    sleep(5)

    def test_full_query_with_lexform(self):
        corp = self.corp_type('дак ты', 1, text='lexform')
        corp.request_examples()

        assert len(corp) > 1
        sleep(5)

    def test_mycorp(self):
        corp = self.corp_type(
            'ты', 1,
            mycorp='JSONeyJkb2NfcmVnaW9uIjogWyLQmtCw0YDQtdC70LjRjyJdfQ%3D%3D'
        )
        corp.request_examples()

        assert len(corp) >= 1
        sleep(5)

    def test_open_graphic(self):
        with pytest.raises(RuntimeError):
            self.corp_normal_obj.open_graphic()
