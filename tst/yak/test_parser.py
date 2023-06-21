import pytest
from unittest.mock import Mock

from yak.yak import ParseError, Parser, Scanner


@pytest.fixture
def parser(src) -> Parser:
    return Parser(Mock(), Scanner(src))


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
