import pytest

from yak.yak import Scanner, ScanError, Token

@pytest.fixture
def scanner(source: str) -> Scanner:
    return Scanner(source)

@pytest.mark.parametrize('source', ['this'])
def test_scan_char_returns_current_char(scanner):
    c = scanner.scan_char()
    assert c == 't'
    assert 0 == scanner.row
    assert 1 == scanner.col
    assert 1 == scanner.pos


@pytest.mark.parametrize('source', ['\nthis'])
def test_scan_char_returns_current_char_handles_new_lines(scanner):
    c = scanner.scan_char()
    assert 1 == scanner.row
    assert 0 == scanner.col
    assert 1 == scanner.pos


@pytest.mark.parametrize('source', [' add 1'])
def test_scan_token_scans_space_delimited_token(scanner):
    token = scanner.scan_token()
    assert token is not None
    assert token == Token('add', 2, 5, 0)


@pytest.mark.parametrize('source', ['"this is a string"'])
def test_scan_token_scans_string_token(scanner):
    token = scanner.scan_token()
    assert token == Token('"this is a string"', 1, 18, 0)


@pytest.mark.parametrize('source', [''])
def test_scan_token_returns_none_at_end_of_the_stream(scanner):
    assert scanner.scan_token() is None


@pytest.mark.parametrize('source', ['       '])
def test_scan_token_returns_null_token_for_empty_source_text(scanner):
    assert scanner.scan_token().null() is True


@pytest.mark.parametrize('source', ['"this'])
def test_scan_token_raises_scanner_error_on_scanning_errors(scanner):
    with pytest.raises(ScanError):
        scanner.scan_token()
