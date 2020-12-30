from time import sleep

import pytest

import rnc.corpora as rnc
from tests.corpora.template import TemplateCorpusTest


class TestMultilingualParaCorpus(TemplateCorpusTest):
    corp_type = rnc.MultilingualParaCorpus

    corp_normal_obj = corp_type('ты', 1, dpp=5, spd=1)
    corp_kwic_obj = corp_type('ты', 1, dpp=5, spd=1, out='kwic')

    corp_normal_obj.request_examples()
    sleep(5)
    corp_kwic_obj.request_examples()
    sleep(5)

    def test_full_query_with_lexform(self):
        corp = self.corp_type('ты готов', 1, text='lexform')
        corp.request_examples()

        assert len(corp) > 1
        sleep(5)

    def test_mycorp(self):
        pass
        # it's impossible to set subcorpus in MultilingualParaCorpus

        # corp = self.corp_type(
        #     'ты', 1,
        #     mycorp='JSONeyJkb2NfaV9sZV9zdGFydF95ZWFyIjogWyIyMDAwIl19'
        # )
        # corp.request_examples()
        #
        # assert len(corp) >= 1
        # sleep(5)

    def test_sort_data(self):
        copy = self.corp_normal_obj.copy()
        copy.sort_data(key=lambda x: len(x.src))

        assert copy.data != self.corp_normal_obj.data

    def test_dump_normal(self):
        with pytest.raises(NotImplementedError):
            super().test_dump_normal()

    def test_dump_kwic(self):
        with pytest.raises(NotImplementedError):
            super().test_dump_kwic()

    def test_load_kwic(self):
        pass

    def test_load_normal(self):
        pass

    def test_load_to_wrong_corpus(self):
        pass

    def test_request_if_base_loaded(self):
        pass

    def test_equality_wordforms_from_rnc_and_from_file(self):
        pass

    def test_found_wordforms_from_file(self):
        pass

    def test_open_graphic(self):
        with pytest.raises(RuntimeError):
            self.corp_normal_obj.open_graphic()
