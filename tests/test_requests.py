import aiohttp
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
    with pytest.raises(ValueError):
        req.get_htmls(RNC_URL, 10, 0)


def test_wrong_params():
    with pytest.raises(aiohttp.ClientResponseError):
        req.get_htmls(RNC_URL, **wrong_params)


def test_incorrect_request():
    with pytest.raises(ValueError):
        req.is_request_correct(RNC_URL, 1, **wrong_params)


def test_correct_request():
    correct_params['lex1'] = 'корпус'
    res = req.is_request_correct(RNC_URL, 1, **correct_params)
    assert res is True


def test_no_results_found():
    wrong_params = correct_params
    wrong_params['lex1'] = 'ssssssssss'

    res = req.whether_result_found(RNC_URL, **wrong_params)
    assert res is False


def test_results_found():
    correct_params['lex1'] = 'ты'
    res = req.whether_result_found(RNC_URL, **correct_params)
    assert res is True


def test_page_does_not_exist():
    wrong_params = correct_params
    wrong_params['lex1'] = 'васкуляризация'

    res = req.does_page_exist(RNC_URL, 10, **wrong_params)
    assert res is False


def test_page_exists():
    correct_params['lex1'] = 'я'
    res = req.does_page_exist(RNC_URL, 20, **correct_params)
    assert res is True


def test_wait_some_time():
    correct_params['lex1'] = 'я'
    html_codes = req.get_htmls(RNC_URL, 0, 15, **correct_params)
    assert len(html_codes) is 15
