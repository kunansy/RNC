from time import sleep

import pytest

import rnc.corpora as rnc
from tests.corpora.template import TemplateCorpusTest


class TestMultimodalCorpus(TemplateCorpusTest):
    corp_type = rnc.MultimodalCorpus

    corp_normal_obj = corp_type('корпус', 1, dpp=5, spd=1)
    corp_kwic_obj = corp_type('корпус', 1, dpp=5, spd=1, out='kwic')

    corp_normal_obj.request_examples()
    sleep(5)
    corp_kwic_obj.request_examples()
    sleep(5)

    def test_download_all(self):
        self.corp_normal_obj.download_all()
        files = os.listdir(self.corp_normal_obj.MEDIA_FOLDER)

        assert all(
            ex.filepath.name in files
            for ex in self.corp_normal_obj
        )

    def test_mycorp(self):
        pass

    def test_open_graphic(self):
        with pytest.raises(RuntimeError):
            self.corp_normal_obj.open_graphic()

    def test_full_query_with_lexform(self):
        corp = self.corp_type('ты это', 1, text='lexform')
        corp.request_examples()

        assert len(corp.data) > 1
