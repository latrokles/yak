import pytest

from yak.parse import Scanner, Token
from yak.parse.scanner import YakScanError, YakScanner


def new_scanner(source: str) -> Scanner:
    return YakScanner(source)


def test_scan_char_returns_current_char():
    scanner = new_scanner('this')
    c = scanner.scan_char()
    assert c == 't'
    assert 0 == scanner.row
    assert 1 == scanner.col
    assert 1 == scanner.pos


def test_scan_char_returns_current_char_handles_new_lines():
    scanner = new_scanner('\nthis')
    c = scanner.scan_char()
    assert 1 == scanner.row
    assert 0 == scanner.col
    assert 1 == scanner.pos


def test_scan_token_scans_space_delimited_token():
    scanner = new_scanner(' add 1')
    token = scanner.scan_token()
    assert token is not None
    assert token == Token('add', 2, 5, 0)


def test_scan_token_scans_string_token():
    source = '"this is a string"'
    scanner = new_scanner(source)
    token = scanner.scan_token()
    assert token == Token(source, 1, 18, 0)


def test_scan_token_returns_none_at_end_of_the_stream():
    source = ''
    assert new_scanner('').scan_token() is None


def test_scan_token_returns_none_for_empty_source_text():
    source = '       '
    assert new_scanner('').scan_token() is None


def test_scan_token_raises_scanner_error_on_scanning_errors():
    with pytest.raises(YakScanError):
        new_scanner('"this').scan_token()
