import pytest

from yak.lang.parse.parser import YakParser, YakParseError
from yak.lang.parse.scanner import YakScanner
from yak.lang.primitives import WordRef
from yak.lang.primitives.task import Task
from yak.lang.vm import YakVirtualMachine


@pytest.fixture
def parser(src) -> YakParser:
    vm = YakVirtualMachine()
    vm.boot_up()

    return YakParser(Task(vm), YakScanner(src))


@pytest.mark.parametrize('src', ['"this is a string"'])
def test_parsing_string_appends_python_string_to_parse_tree(parser):
    parse_tree = parser.parse()
    assert len(parse_tree) == 1
    assert parse_tree[0] == 'this is a string'


@pytest.mark.parametrize('src', ['4.0 5.5 3.14159'])
def test_parsing_floats_appends_python_floats_to_parse_tree(parser):
    parse_tree = parser.parse()
    assert parse_tree == [4.0, 5.5, 3.14159]


@pytest.mark.parametrize('src', ['4 5 3'])
def test_parsing_ints_appends_python_ints_to_parse_tree(parser):
    parse_tree = parser.parse()
    assert parse_tree == [4, 5, 3]


@pytest.mark.parametrize('src', ['t f nil'])
def test_parsing_words_appends_a_word_reference_to_parse_tree(parser):
    parse_tree = parser.parse()
    assert parse_tree == [WordRef('t'), WordRef('f'), WordRef('nil')]


@pytest.mark.parametrize('src', ['frobulate'])
def test_parsing_words_raises_parse_error_if_word_is_not_defined(parser):
    with pytest.raises(YakParseError):
        parse_tree = parser.parse()
