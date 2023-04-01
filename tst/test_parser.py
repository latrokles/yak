import pytest

from yak.interpreter import Interpreter
from yak.parsing import Parser, ParseError, Scanner
from yak.primitives import WordRef
from yak.primitives.quotation import Quotation
from yak.vm import YakVirtualMachine


@pytest.fixture
def parser(src) -> Parser:
    vm = YakVirtualMachine()
    vm.init()

    return Parser(Interpreter(vm), Scanner(src))


@pytest.mark.parametrize('src', ['"this is a string"'])
def test_parsing_string_appends_python_string_to_parse_tree(parser):
    parse_tree = parser.parse()
    assert parse_tree.count == 1
    assert parse_tree[0] == 'this is a string'


@pytest.mark.parametrize('src', ['4.0 5.5 3.14159'])
def test_parsing_floats_appends_python_floats_to_parse_tree(parser):
    parse_tree = parser.parse()
    assert parse_tree == Quotation([4.0, 5.5, 3.14159])


@pytest.mark.parametrize('src', ['4 5 3'])
def test_parsing_ints_appends_python_ints_to_parse_tree(parser):
    parse_tree = parser.parse()
    assert parse_tree == Quotation([4, 5, 3])


@pytest.mark.parametrize('src', ['t f nil'])
def test_parsing_words_appends_a_word_reference_to_parse_tree(parser):
    parse_tree = parser.parse()
    assert parse_tree == Quotation([WordRef('t'), WordRef('f'), WordRef('nil')])


@pytest.mark.parametrize('src', ['frobulate'])
def test_parsing_words_raises_parse_error_if_word_is_not_defined(parser):
    with pytest.raises(ParseError):
        parse_tree = parser.parse()
