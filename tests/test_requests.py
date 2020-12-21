import pytest

import rnc.corpora_requests as req
from rnc.corpora import RNC_URL

correct_params = {
    'env': 'alpha',
    'api': '1.0',
    'lang': 'ru',
    'mode': 'main',
    'text': 'lexgramm',
    'out': 'normal',
}
wrong_params = {
    'shue': 'ppsh'
}


def test_wrong_range():
    assert len(req.get_htmls(RNC_URL, 10, 0)) == 0


def test_wrong_params():
    req.get_htmls(RNC_URL, **wrong_params)


def test_incorrect_request():
    with pytest.raises(ValueError):
        req.is_request_correct(RNC_URL, 1, **wrong_params)


def test_wait_some_time():
    correct_params['lex1'] = 'я'
    html_codes = req.get_htmls(RNC_URL, 0, 15, **correct_params)
    assert len(html_codes) is 15
