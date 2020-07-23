import pytest
from src.corpora import MainCorpus


def test_correct_req_with_lexform():
    corp = MainCorpus('слово', 1, text='lexform', spd=1,
                      dpp=1, marker=lambda x: f"<b>{x}</b>")
    corp.request_examples()
    assert corp.p_count == 1


def test_incorrect_gramm_request():
    corp = MainCorpus({"слово": {'gramm': 'V'}}, 1, dpp=1, spd=1, marker=None)
    with pytest.raises(ValueError):
        corp.request_examples()


def test_page_does_not_exist():
    corp = MainCorpus(
        'ыыыыыыыыыыыыыыыыы', 1, dpp=1, spd=1, marker=lambda x: f"**{x}**")
    with pytest.raises(ValueError):
        corp.request_examples()


def test_correct_req():
    corp = MainCorpus(
        {'охотник': {'gramm': {'case': ['nom', 'gen', 'dat']}, 'numberus': 'sg'},
         'видеть': {'gramm': {'mood': 'partcp'}, 'min': 1, 'max': 5}},
        1, dpp=2, spd=10, marker=str.upper)
    corp.request_examples()
    assert corp.data


def test_kwic():
    corp = MainCorpus({'мы': {'gramm': 'acc'}}, 1,
                      out='kwic', expand='full', marker=str.upper)
    corp.request_examples()


if __name__ == '__main__':
    pass
    # test_kwic()
    # test_correct_req()
    # test_page_does_not_exist()
    # test_incorrect_gramm_request()
    # test_correct_req_with_lexform()
