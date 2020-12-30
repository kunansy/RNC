import rnc.corpora_params as params

import pytest

mycorp = params.Mycorp()


def test_get_correct_language_key():
    assert mycorp.en == mycorp.English == mycorp['en'] == mycorp['English'] == \
           mycorp.Parallel.English == mycorp.Parallel.en


def test_get_wrong_lang_attr():
    with pytest.raises(AttributeError):
        mycorp.engl

    with pytest.raises(AttributeError):
        mycorp.Parallel.engl


def test_get_wrong_lang_item():
    with pytest.raises(KeyError):
        mycorp['engl']


def test_get_correct_person_key():
    assert mycorp.Pushkin == mycorp['Pushkin'] == mycorp.Person.Pushkin


def test_get_wrong_person_key():
    with pytest.raises(AttributeError):
        mycorp.Person.push
