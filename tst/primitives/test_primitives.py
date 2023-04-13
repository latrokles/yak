from yak.primitives import prettyformat
from yak.primitives.quotation import Quotation


def test_prettyformat_returns_string_representation_of_values():
    assert prettyformat(None) == 'nil'
    assert prettyformat(True) == 't'
    assert prettyformat(False) == 'f'
    assert prettyformat(Quotation()) == '[ ]'
    assert prettyformat(1) == '1'
    assert prettyformat(1.0) == '1.0'
