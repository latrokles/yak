import pytest

from yak.parsing import Parser, ParseError, Scanner
from yak.primitives.word import WordRef
from yak.primitives.quotation import Quotation
from yak.util import get_logger


@pytest.fixture
def parser(src) -> Parser:
    return Parser(Interpreter(get_logger('INFO')).init(), Scanner(src))


@pytest.mark.skip()
@pytest.mark.parametrize('src', ['"this is a string"'])
def test_parsing_string_appends_python_string_to_parse_tree(parser):
    parse_tree = parser.parse()
    assert parse_tree.count == 1
    assert parse_tree[0] == 'this is a string'


@pytest.mark.skip()
@pytest.mark.parametrize('src', ['4.0 5.5 3.14159'])
def test_parsing_floats_appends_python_floats_to_parse_tree(parser):
    parse_tree = parser.parse()
    assert parse_tree == Quotation([4.0, 5.5, 3.14159])


@pytest.mark.skip()
@pytest.mark.parametrize('src', ['4 5 3'])
def test_parsing_ints_appends_python_ints_to_parse_tree(parser):
    parse_tree = parser.parse()
    assert parse_tree == Quotation([4, 5, 3])


@pytest.mark.skip()
@pytest.mark.parametrize('src', ['t f nil'])
def test_parsing_words_appends_a_word_reference_to_parse_tree(parser):
    parse_tree = parser.parse()
    assert parse_tree == Quotation([WordRef('t', 'syntax'), WordRef('f', 'syntax'), WordRef('nil', 'syntax')])


@pytest.mark.skip()
@pytest.mark.parametrize('src', ['frobulate'])
def test_parsing_words_raises_parse_error_if_word_is_not_defined(parser):
    with pytest.raises(ParseError):
        parse_tree = parser.parse()