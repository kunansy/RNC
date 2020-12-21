import os
from pathlib import Path

import pytest

import rnc.corpora as corp
import rnc.corpora_params as params
import rnc.examples as expl


class TemplateTestExamples:
    ex = expl.Example

    def test_text_getter(self):
        assert isinstance(self.ex.txt, str) and self.ex.txt

    def test_text_setter(self):
        copy = self.ex.copy()
        new_txt = 'test_text'
        copy.txt = new_txt

        assert copy.txt == new_txt

    def test_text_setter_with_notstr_type(self):
        copy = self.ex.copy()
        new_txt = list('new ex')
        copy.txt = new_txt

        assert copy.txt == new_txt

    def test_src_getter(self):
        assert isinstance(self.ex.src, str) and self.ex.src

    def test_src_setter(self):
        copy = self.ex.copy()
        new_src = 'test_source'
        copy.src = new_src

        assert copy.src == new_src

    def test_src_setter_with_notstr_type(self):
        copy = self.ex.copy()
        new_src = list('test_source')
        copy.src = new_src

        assert copy.src == new_src

    def test_ambiguation_getter(self):
        amb = self.ex.ambiguation

        assert isinstance(amb, str) and amb

    def test_ambiguation_setter(self):
        copy = self.ex.copy()
        new_amb = 'new_amb'
        copy.ambiguation = new_amb

        assert copy.ambiguation == new_amb

    def test_ambiguation_setter_with_nostr_type(self):
        copy = self.ex.copy()
        new_amb = list('new_amb')
        copy.ambiguation = new_amb

        assert copy.ambiguation == new_amb

    def test_doc_url(self):
        url = self.ex.doc_url

        assert isinstance(url, str) and url

    def test_found_worforms(self):
        wf = self.ex.found_wordforms

        assert isinstance(wf, list) and wf

    def test_columns(self):
        columns = self.ex.columns
        expected = ['text', 'source', 'ambiguation', 'found wordforms', 'URL']

        assert columns == expected

    def test_items(self):
        items = self.ex.items

        assert all(
            isinstance(i, str) and i
            for i in items
        )

    def test_data(self):
        data = self.ex.data

        assert isinstance(data, dict) and len(data) is 4

    def test_open_doc(self):
        self.ex.open_doc()

    def test_mark_words(self):
        txt_template = "{}, aghA{}12g_HGH g,.,,{},.,a{}s agsd :'{}'!"
        copy = self.ex.copy()
        word = copy.found_wordforms[0]

        new_txt = txt_template.format(*([word] * 5))
        expected_txt = txt_template.format(
            word.upper(), word, word.upper(), word, word.upper())

        copy.txt = new_txt
        copy.mark_found_words(str.upper)

        assert copy.txt == expected_txt

    def test_deleter(self):
        with pytest.raises(AttributeError):
            del self.ex.txt

    def test_copy(self):
        assert self.ex == self.ex.copy()

    def test_contains(self):
        item = self.ex.txt[:5]

        assert item in self.ex

    def test_contains_with_notstr_type(self):
        copy = self.ex.copy()
        copy.txt = ['1', 2, 3, 4, '5']

        assert '1' in copy and 2 in copy

    def test_equal(self):
        lhs = rhs = self.ex.copy()
        lhs.txt = list('test lhs')
        rhs.txt = lhs.txt

        assert lhs == rhs


class TestMainExample(TemplateTestExamples):
    corpus_res = corp.MainCorpus('тест', 1, marker=str.upper)
    corpus_res.request_examples()
    ex: expl.MainExample = corpus_res[0]


class TestKwicExample(TemplateTestExamples):
    corpus_res = corp.MainCorpus('тест', 1, marker=str.upper, out='kwic')
    corpus_res.request_examples()
    ex: expl.KwicExample = corpus_res[0]

    def test_text_setter(self):
        with pytest.raises(NotImplementedError):
            self.ex.txt = 'sth'

    def test_text_setter_with_notstr_type(self):
        with pytest.raises(NotImplementedError):
            self.ex.txt = 123

    def test_left_setter(self):
        copy = self.ex.copy()
        new_left = 'new left'
        copy.left = new_left

        assert copy.left == new_left

    def test_left_setter_with_notstr_type(self):
        copy = self.ex.copy()
        new_left = list('new left')
        copy.left = new_left

        assert copy.left == new_left

    def test_center_setter(self):
        copy = self.ex.copy()
        new_center = 'new center'
        copy.center = new_center

        assert copy.center == new_center

    def test_center_setter_with_notstr_type(self):
        copy = self.ex.copy()
        new_center = list('new center')
        copy.center = new_center

        assert copy.center == new_center

    def test_right_setter(self):
        copy = self.ex.copy()
        new_right = 'new right'
        copy.right = new_right

        assert copy.right == new_right

    def test_right_setter_with_notstr_type(self):
        copy = self.ex.copy()
        new_right = list('new right')
        copy.right = new_right

        assert copy.right == new_right

    def test_ambiguation_getter(self):
        with pytest.raises(NotImplementedError):
            amb = self.ex.ambiguation

    def test_ambiguation_setter(self):
        with pytest.raises(AttributeError):
            self.ex.ambiguation = 'sth'

    def test_ambiguation_setter_with_nostr_type(self):
        with pytest.raises(AttributeError):
            self.ex.ambiguation = 123

    def test_columns(self):
        columns = self.ex.columns
        expected = ['left', 'center', 'right', 'source',
                    'found wordforms', 'URL']

        assert columns == expected

    def test_data(self):
        data = self.ex.data

        assert isinstance(data, dict) and len(data) is 5

    def test_mark_words(self):
        txt_template = "{}, aghA{}12g_HGH g,.,,{},.,a{}s agsd :'{}'!"
        copy = self.ex.copy()
        word = copy.found_wordforms[0]

        new_txt = txt_template.format(*([word] * 5))
        expected_txt = txt_template.format(
            word.upper(), word, word.upper(), word, word.upper())

        copy.left = copy.center = copy.right = new_txt
        copy.mark_found_words(str.upper)

        assert copy.left == copy.center == copy.right == expected_txt

    def test_contains_with_notstr_type(self):
        copy = self.ex.copy()
        copy.left = [1, 2, 3]
        copy.center = '1'
        copy.right = 12

        assert '12' in copy

    def test_equal(self):
        lhs = rhs = self.ex.copy()
        lhs.left = rhs.left = ''

        assert lhs == rhs


class TestParallelExample(TemplateTestExamples):
    mycorp = params.Mycorp()
    corpus_res = corp.ParallelCorpus(
        'тест', 1, marker=str.upper, subcorpus=mycorp.en)

    corpus_res.request_examples()
    ex: expl.ParallelExample = corpus_res[0]

    def test_text_getter(self):
        txt = self.ex.txt

        assert isinstance(txt, dict) and len(txt) is 2

    def test_text_setter(self):
        with pytest.raises(NotImplementedError):
            self.ex.txt = {}

    def test_text_setter_with_notstr_type(self):
        with pytest.raises(NotImplementedError):
            self.ex.txt = 12

    def test_data(self):
        data = self.ex.data

        assert isinstance(data, dict) and len(data) is 5

    def test_iadd_with_nochanges(self):
        copy = self.ex.copy()
        new_ex = expl.ParallelExample()
        copy += new_ex

        assert copy == self.ex

    def test_iadd_with_extend_texts(self):
        txt = {
            'ru': 'текст1',
            'en': 'text1'
        }
        lhs = expl.ParallelExample(txt, 'old_src', 'not amb', ['test'])

        update = {
            'ru': 'и текст2',
            'en': 'and text2'
        }
        rhs = expl.ParallelExample(update, 'old src | new src', 'amb', ['test1'])
        lhs += rhs

        assert lhs.ru == 'текст1 и текст2'
        assert lhs.en == 'text1 and text2'
        assert lhs.src == 'old src | new src'
        assert lhs.ambiguation == 'amb'
        assert lhs.found_wordforms == ['test', 'test1']

    def test_iadd_with_new_lang(self):
        txt = {
            'ru': 'текст1',
            'en': 'text1'
        }
        lhs = expl.ParallelExample(txt, 'old src | new src', 'amb', ['test'])

        update = {
            'fr': 'и текст2',
            'ch': 'and text2'
        }
        rhs = expl.ParallelExample(update, 'new src', 'not amb', [])
        lhs += rhs

        assert lhs.ru == 'текст1'
        assert lhs.en == 'text1'
        assert lhs.fr == 'и текст2'
        assert lhs.ch == 'and text2'
        assert lhs.src == 'old src | new src'
        assert lhs.ambiguation == 'amb'
        assert lhs.found_wordforms == ['test']

    def test_iadd_with_new_lang_and_extend_texts(self):
        txt = {
            'ru': 'текст1',
            'en': 'text1'
        }
        lhs = expl.ParallelExample(txt, 'old src', 'not amb', ['test'])

        update = {
            'ru': 'и текст2',
            'en': 'and text2',
            'fr': 'и текст3',
            'ch': 'and text3'
        }
        rhs = expl.ParallelExample(update, '', '', ['text1'])
        lhs += rhs

        assert lhs.ru == 'текст1 и текст2'
        assert lhs.en == 'text1 and text2'
        assert lhs.fr == 'и текст3'
        assert lhs.ch == 'and text3'
        assert lhs.src == 'old src'
        assert lhs.ambiguation == 'not amb'
        assert lhs.found_wordforms == ['test', 'text1']

    def test_iadd_with_update_ambiguation_from_null(self):
        txt = {
            'ru': 'текст1',
            'en': 'text1'
        }
        lhs = expl.ParallelExample(txt, 'old src', '', [])

        update = {
            'fr': 'и текст2',
            'ch': 'and text2'
        }
        rhs = expl.ParallelExample(update, 'new src', 'not amb', [])
        lhs += rhs

        assert lhs.ru == 'текст1'
        assert lhs.en == 'text1'
        assert lhs.fr == 'и текст2'
        assert lhs.ch == 'and text2'
        assert lhs.src == 'old src'
        assert lhs.ambiguation == 'not amb'
        assert lhs.found_wordforms == []

    def test_columns(self):
        columns = self.ex.columns
        expected = ['en', 'ru', 'source', 'ambiguation',
                    'found wordforms', 'URL']

        assert columns == expected

    def test_getattr(self):
        txt = self.ex.ru

        assert isinstance(txt, str) and txt

    def test_getattr_none(self):
        assert self.ex.fr is None

    def test_getitem(self):
        txt = self.ex['ru']

        assert isinstance(txt, str) and txt

    def test_getitem_none(self):
        assert self.ex['fr'] is None

    def test_setitem(self):
        new_txt = 'sth with new txt'
        copy = self.ex.copy()
        copy['ru'] = new_txt

        assert copy.ru == new_txt

    def test_setitem_with_notstr_type(self):
        copy = self.ex.copy()
        new_txt = list('new txt')
        copy['ru'] = new_txt

        assert copy.ru == new_txt

    def test_sort(self):
        copy = self.ex.copy()
        copy.sort()

        assert copy.txt == self.ex.txt

    def test_mark_words(self):
        txt_template = "{}, aghA{}12g_HGH g,.,,{},.,a{}s agsd :'{}'!"
        copy = self.ex.copy()
        word = copy.found_wordforms[0]

        new_txt = txt_template.format(*([word] * 5))
        expected_txt = txt_template.format(
            word.upper(), word, word.upper(), word, word.upper())

        copy['ru'] = new_txt
        copy.mark_found_words(str.upper)

        assert copy.ru == expected_txt

    def test_equality(self):
        assert self.ex['ru'] == self.ex.ru

    def test_equal(self):
        lhs = rhs = self.ex.copy()
        lhs['fr'] = rhs['fr'] = ''

        assert lhs == rhs

    def test_contains(self):
        text = self.ex.ru[:5]

        assert text in self.ex

    def test_contains_with_notstr_type(self):
        copy = self.ex.copy()
        new_txt = ['1', 2, '3', '5']
        copy['ru'] = new_txt

        assert '1' in copy and '3' in copy


class TestMultimodalExample(TemplateTestExamples):
    corpus_res = corp.MultimodalCorpus(
        'корпус', 1, marker=str.upper)
    corpus_res.request_examples()
    ex: expl.MultimodalExample = corpus_res[0]

    def test_columns(self):
        columns = self.ex.columns
        expected = ['text', 'source', 'ambiguation',
                    'found wordforms', 'URL', 'media_url', 'filename']

        assert columns == expected

    def test_items(self):
        items = self.ex.items

        assert all(isinstance(i, (str, Path)) and i for i in items)

    def test_download_file(self):
        self.ex.download_file()
        files = os.listdir(f'data{os.sep}media')

        assert self.ex.filepath.name in files

    def test_filepath_getter(self):
        path = self.ex.filepath

        assert isinstance(path, Path)

    def test_filepath_setter(self):
        self.ex.filepath = 'path'
