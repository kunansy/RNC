import rnc.corpora as corp
import rnc.examples as expl
import pytest


class TemplateTestExamples:
    ex = expl.Example

    def test_text_getter(self):
        assert isinstance(self.ex.txt, str) and self.ex.txt

    def test_text_setter(self):
        copy = self.ex.copy()
        new_txt = 'test_text'
        copy.txt = new_txt
        assert copy.txt == new_txt

    def test_src(self):
        assert isinstance(self.ex.src, str) and self.ex.src

    def test_ambiguation_getter(self):
        amb = self.ex.ambiguation
        assert isinstance(amb, str) and amb

    def test_ambiguation_setter(self):
        copy = self.ex.copy()
        new_amb = 'new_amb'
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
        assert all(isinstance(i, str) and i for i in items)

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

    def test_normal_copy(self):
        assert self.ex == self.ex.copy()


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

    def test_ambiguation_getter(self):
        with pytest.raises(NotImplementedError):
            amb = self.ex.ambiguation

    def test_ambiguation_setter(self):
        with pytest.raises(AttributeError):
            self.ex.ambiguation = 'sth'

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


class TestParallelExample(TemplateTestExamples):
    corpus_res = corp.ParallelCorpus(
        'тест', 1, marker=str.upper, subcorpus=corp.Subcorpus.Parallel.English)
    corpus_res.request_examples()
    ex: expl.ParallelExample = corpus_res[0]

    def test_text_getter(self):
        txt = self.ex.txt
        assert isinstance(txt, dict) and len(txt) is 2

    def test_text_setter(self):
        with pytest.raises(NotImplementedError):
            self.ex.txt = {}

    def test_data(self):
        data = self.ex.data
        assert isinstance(data, dict) and len(data) is 5

    def test_iadd(self):
        # TODO
        pass

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