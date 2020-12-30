import os
from pathlib import Path
from time import sleep

import pytest

import rnc.corpora as rnc


class TemplateCorpusTest:
    corp_type = rnc.Corpus

    corp_normal_obj = None
    corp_kwic_obj = None

    full_query = {
        'ты': {
            'gramm': {
                'case': ['acc', 'nom', 'gen'],
                'num': ['sg', 'pl']
            },
            'flags': {
                'position': ['amark', 'bmark'],
            }
        }
    }

    #########################
    #    Test requesting    #
    #########################

    def test_empty_query(self):
        with pytest.raises(ValueError):
            self.corp_type('', 1, marker=str.upper)

    def test_p_count_zero(self):
        with pytest.raises(ValueError):
            self.corp_type('корпус', 0, marker=None)

    def test_one_str_with_one_word(self):
        corp = self.corp_type('ты', 1, marker=str.capitalize, spd=1, dpp=5)
        corp.request_examples()

        assert len(corp) > 1
        sleep(5)

    def test_one_form_without_gram(self):
        corp = self.corp_type({'ты': ''}, 1, marker=str.capitalize, spd=1, dpp=5)
        corp.request_examples()

        assert len(corp) > 1
        sleep(5)

    def test_one_form_with_one_gram(self):
        corp = self.corp_type({'ты': {'gramm': 'nom'}}, 1, marker=str.capitalize, spd=1)
        corp.request_examples()

        assert len(corp) > 1
        sleep(5)

    def test_one_form_with_grams_and_flags(self):
        query = {
            'ты': {
                'gramm': 'acc',
                'flags': 'amark'
            }
        }
        corp = self.corp_type(query, 1, marker=str.capitalize)
        corp.request_examples()

        assert len(corp) > 1
        sleep(5)

    def test_one_form_with_several_grams_and_flags(self):
        corp = self.corp_type(self.full_query, 1, marker=str.capitalize)
        corp.request_examples()

        assert len(corp) > 1
        sleep(5)

    def test_full_query_with_lexform(self):
        corp = self.corp_type('слово бога', 1, text='lexform')
        corp.request_examples()

        assert len(corp) > 1
        sleep(5)

    def test_full_query_with_kwic_without_kwsz(self):
        corp = self.corp_type(self.full_query, 1, marker=str.capitalize, out='kwic')
        corp.request_examples()

        assert len(corp) > 1
        sleep(5)

    def test_full_query_with_kwic_with_kwsz(self):
        corp = self.corp_type(self.full_query, 1, marker=str.capitalize, out='kwic', kwsz=7)
        corp.request_examples()

        assert len(corp) > 1
        sleep(5)

    def test_sort_in_request(self):
        default = self.corp_type('ты', 1)
        default.request_examples()
        sleep(5)

        by_creation_date = self.corp_type('ты', 1, sort='i_grcreated_inv')
        by_creation_date.request_examples()
        sleep(5)

        assert default.data != by_creation_date.data

    def test_mycorp(self):
        corp = self.corp_type(
            'ты', 1,
            mycorp="JSONeyJkb2Nfc2V4IjogWyLQvNGD0LYiXSwgImRvY19pX3RhZ2dpbmciOiBbIjEiXX0%3D"
        )
        corp.request_examples()

        assert len(corp) >= 1
        sleep(5)

    def test_call(self):
        corp = self.corp_type('ты', 1, marker=str.capitalize, out='kwic')
        corp()

        assert len(corp) > 1

    #########################
    #   Working with file   #
    #########################

    def test_dump_normal(self):
        self.corp_normal_obj.dump()

    def test_dump_kwic(self):
        self.corp_kwic_obj.dump()

    def test_load_normal(self):
        corp = self.corp_type(file=self.corp_normal_obj.file)

        assert len(corp) == len(self.corp_normal_obj)
        assert (
            from_file == from_corp
            for from_file, from_corp in zip(corp, self.corp_normal_obj)
        )

    def test_load_kwic(self):
        corp = self.corp_type(file=self.corp_kwic_obj.file)

        assert len(corp) == len(self.corp_kwic_obj)
        assert (
            from_file == from_corp
            for from_file, from_corp in zip(corp, self.corp_kwic_obj)
        )

    def test_load_to_wrong_corpus(self):
        with pytest.raises(NotImplementedError):
            self.corp_type(file=f'data{os.sep}wrong_mode.csv')

    def test_request_if_base_loaded(self):
        corp = self.corp_type(file=self.corp_normal_obj.file)
        with pytest.raises(RuntimeError):
            corp.request_examples()

    def test_default_filetype(self):
        corp = self.corp_type('ты', 1)

        assert isinstance(corp.file, Path) and corp.file.suffix == '.csv'

    def test_equality_wordforms_from_rnc_and_from_file(self):
        corp = self.corp_type(file=self.corp_kwic_obj.file)

        assert all(
            from_file == from_corp
            for from_file, from_corp in zip(corp, self.corp_kwic_obj)
        )

    #########################
    #    Test properties    #
    #########################

    def test_data_type(self):
        assert isinstance(self.corp_normal_obj.data, list)

    def test_data_elements_type(self):
        assert all(
            isinstance(ex, self.corp_normal_obj.ex_type)
            for ex in self.corp_normal_obj
        )

    def test_query_dict(self):
        corp = self.corp_type({'ты': {'gramm': 'acc'}}, 1)

        assert isinstance(corp.query, dict) and corp.query

    def test_query_str(self):
        corp = self.corp_type('ты', 1)

        assert isinstance(corp.query, str) and corp.query

    def test_forms_in_query_dict(self):
        corp = self.corp_type({'ты': {'gramm': 'acc'}, 'готов': {}}, 1)

        assert isinstance(corp.forms_in_query, list)
        assert all(isinstance(form, str) for form in corp.forms_in_query)
        assert len(corp.forms_in_query) is 2
        assert corp.forms_in_query == ['ты', 'готов']

    def test_forms_in_query_str(self):
        corp = self.corp_type('ты готов ', 1)

        assert isinstance(corp.forms_in_query, list)
        assert all(isinstance(form, str) for form in corp.forms_in_query)
        assert len(corp.forms_in_query) is 2
        assert corp.forms_in_query == ['ты', 'готов']

    def test_p_count(self):
        corp = self.corp_type('ты', 1)

        assert corp.p_count is 1

    def test_found_wordforms_from_file(self):
        corp = self.corp_type(file=self.corp_normal_obj.file)

        assert corp.found_wordforms == self.corp_normal_obj.found_wordforms

    def test_url(self):
        corp = self.corp_type('ты', 1)

        assert isinstance(corp.url, str) and corp.url

    def test_amount_of_docs_normal(self):
        assert isinstance(self.corp_normal_obj.amount_of_docs, int)

    def test_amount_of_docs_kwic(self):
        assert self.corp_kwic_obj.amount_of_docs is None

    def test_amount_of_contexts_normal(self):
        assert isinstance(self.corp_normal_obj.amount_of_contexts, int)

    def test_amount_of_contexts_kwic(self):
        assert isinstance(self.corp_kwic_obj.amount_of_contexts, int)

    ##########################
    # Test working with data #
    ##########################

    def test_open_url(self):
        self.corp_normal_obj.open_url()

    def test_open_graphic(self):
        self.corp_normal_obj.open_graphic()

    def test_copy(self):
        copy = self.corp_normal_obj.copy()

        assert copy.data == self.corp_normal_obj.data

    def test_sort_data(self):
        copy = self.corp_normal_obj.copy()
        copy.sort_data(key=lambda x: len(x.txt))

        assert copy.data != self.corp_normal_obj.data

    def test_pop(self):
        copy = self.corp_normal_obj.copy()
        example = copy.pop(0)

        assert any(
            example == ex
            for ex in self.corp_normal_obj)
        assert all(
            example != ex
            for ex in copy
        )

    def test_contains(self):
        copy = self.corp_normal_obj.copy()
        example = copy.pop(0)

        assert (example in self.corp_normal_obj and
                example not in copy)

    def test_shuffle(self):
        copy = self.corp_normal_obj.copy()
        copy.shuffle()

        assert copy.data != self.corp_normal_obj.data

    def test_clear(self):
        copy = self.corp_normal_obj.copy()
        copy.clear()

        assert not copy.data
        assert copy.query
        assert copy.p_count
        assert copy.params

    def test_filter(self):
        copy = self.corp_normal_obj.copy()
        copy.filter(lambda x: x.txt is None)

        assert len(copy) == 0

    def test_getattr_normal(self):
        mode = self.corp_normal_obj.mode

        assert isinstance(mode, str) and mode

    def test_getattr_none(self):
        assert self.corp_normal_obj.name is None

    def test_getitem_one(self):
        item = self.corp_normal_obj[0]

        assert item in self.corp_normal_obj

    def test_getitem_slice(self):
        sliced = self.corp_normal_obj[::-1]

        assert all(
            lhs == rhs
            for lhs, rhs in zip(self.corp_normal_obj.data[::-1], sliced)
        )

    def test_delitem(self):
        copy = self.corp_normal_obj.copy()
        del copy[:]

        assert len(copy.data) == 0

    ##########################
    #   Test class setters   #
    ##########################

    def test_set_spd_normal(self):
        self.corp_type.set_spd(20)
        corp = self.corp_type('ты', 1)

        assert corp.spd is 20

    def test_set_spd_exception(self):
        with pytest.raises(ValueError):
            self.corp_type.set_spd('12')

    def test_set_dpp_normal(self):
        self.corp_type.set_dpp(20)
        corp = self.corp_type('ты', 1)

        assert corp.dpp is 20

    def test_set_dpp_exception(self):
        with pytest.raises(ValueError):
            self.corp_type.set_dpp('12')

    def test_set_text_normal(self):
        self.corp_type.set_text('lexform')
        corp = self.corp_type('ты', 1)

        assert corp.text == 'lexform'

    def test_set_text_exception(self):
        with pytest.raises(ValueError):
            self.corp_type.set_text(12)

    def test_set_sort_normal(self):
        self.corp_type.set_sort('i_grcreated_inv')
        corp = self.corp_type('ты', 1)

        assert corp.sort == 'i_grcreated_inv'

    def test_set_sort_exception(self):
        with pytest.raises(ValueError):
            self.corp_type.set_sort(12)

    def test_set_min_normal(self):
        self.corp_type.set_min(10)
        corp = self.corp_type('ты готов', 1)

        assert corp.min2 is 10

    def test_set_min_exception(self):
        with pytest.raises(ValueError):
            self.corp_type.set_min('12')

    def test_set_max_normal(self):
        self.corp_type.set_max(10)
        corp = self.corp_type('ты готов', 1)

        assert corp.max2 is 10

    def test_set_max_exception(self):
        with pytest.raises(ValueError):
            self.corp_type.set_max('12')

    def test_set_restrict_show_exception_str(self):
        with pytest.raises(TypeError):
            self.corp_type.set_restrict_show('False')

    def test_set_restrict_show_exception_list(self):
        with pytest.raises(TypeError):
            self.corp_type.set_restrict_show([False])
