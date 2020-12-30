from time import sleep

import pytest

import rnc.corpora as rnc
from tests.corpora.template import TemplateCorpusTest


class TestAccentologicalCorpus(TemplateCorpusTest):
    corp_type = rnc.AccentologicalCorpus

    corp_normal_obj = corp_type('ты', 1, dpp=5, spd=1)
    corp_kwic_obj = corp_type('ты', 1, dpp=5, spd=1, out='kwic')

    corp_normal_obj.request_examples()
    sleep(5)
    corp_kwic_obj.request_examples()
    sleep(5)

    def test_mycorp(self):
        corp = self.corp_type(
            'ты', 1,
            mycorp='JSONeyJkb2NfYXV0aG9yIjogWyLQkC7QoS4g0J_Rg9GI0LrQuNC9Il0sICJkb2NfaV9sZV9lbmRfeWVhciI6IFsiMTgzMCJdfQ%3D%3D'
        )
        corp.request_examples()

        assert len(corp) >= 1
        sleep(5)

    def test_open_graphic(self):
        with pytest.raises(RuntimeError):
            self.corp_normal_obj.open_graphic()
