from yak.lang.primitives.kernel import print_object
from yak.lang.primitives.quotation import Quotation


def test_print_object_returns_string_representation_of_values():
    assert print_object(None) == 'nil'
    assert print_object(True) == 't'
    assert print_object(False) == 'f'
    assert print_object(Quotation()) == '[ ]'
    assert print_object(1) == '1'
    assert print_object(1.0) == '1.0'
