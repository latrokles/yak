import pytest

from yak.primitives import Value
from yak.primitives.quotation import Quotation


@pytest.fixture
def quote(values: list[Value]) -> Quotation:
    return Quotation(values)


@pytest.mark.parametrize('values', [[1, 2, 3, 4]])
def test_count_returns_number_of_elements_in_quotation(quote):
    assert quote.count == 4


@pytest.mark.parametrize('values', [[]])
def test_empty_returns_true_if_quotation_is_empty(quote):
    assert quote.empty is True


@pytest.mark.parametrize('values', [[1, 2, 3, 4]])
def test_empty_returns_false_if_quotation_is_not_empty(quote):
    assert quote.empty is False


@pytest.mark.parametrize('values', [[1, 2, 3, 4]])
def test_head_returns_first_element_of_quotation(quote):
    assert quote.head == 1


@pytest.mark.parametrize('values', [[]])
def test_head_returns_none_if_quotation_is_empty(quote):
    assert quote.head is None


@pytest.mark.parametrize('values', [[1, 2, 3, 4]])
def test_tail_returns_quotation_without_its_first_value(quote):
    assert quote.tail == Quotation([2, 3, 4])


@pytest.mark.parametrize('values', [[]])
def test_tail_returns_empty_quotation_if_quotation_is_empty(quote):
    assert quote.tail == Quotation()


@pytest.mark.parametrize('values', [[1, 2, 3, 4]])
def test_print_object_returns_string_representation_of_the_quotation(quote):
    assert quote.print_object() == '[ 1 2 3 4 ]'
