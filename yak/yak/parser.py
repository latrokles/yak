import enum

from contextlib import contextmanager

from .scanner import Token
from .core import Stack, YakError, YakVal


def is_null(token: Token|None) -> bool:
    return token is None or token.null()


def is_int(val: str) -> bool:
    try:
        int(val)
        return True
    except ValueError:
        return False


def is_float(val: str) -> bool:
    try:
        float(val)
        return True
    except ValueError:
        return False


def is_string(val: str) -> bool:
    val = str(val)
    return val.startswith('"') and val.endswith('"')


class ParseError(YakError):
    """Raised when the parser is unable to parse the tokens scanned."""


@enum.unique
class ParseMode(enum.Enum):
    PARSE = 'PARSE'
    STRING = 'STRING'


class Parser:
    EOF = '#EOF#'

    def __init__(self, runtime, scanner):
        self.runtime = runtime
        self.scanner = scanner
        self.in_exclusive_def = False
        self.mode = ParseMode.PARSE
        self.data = Stack()
        self.expected_defn = Stack
        self.vocab = None
        self.push([])

    def parse(self) -> list[YakVal]:
        while (value := self.next_value()) != Parser.EOF:
            self.accumulator.append(value)
        return self.accumulator

    def next_value(self) -> YakVal:
        try:
            if is_null((token := self.scanner.scan_token())):
                return Parser.EOF
            return self.parse_value(token)
        except ParseError:
            raise
        except Exception as e:
            raise ParseError(f'Unable to parse token={token}, error={e}')

    def parse_value(self, token: Token) -> YakVal:
        if is_int(token.text):
            return int(token.text)

        if is_float(token.text):
            return float(token.text)

        if is_string(token.text):
            return token.text[1:-1]

        raise ParseError(f'Unable to parse token={token}')

    def peek(self):
        return self.data.peek()

    def pop(self):
        return self.data.pop()

    def push(self, value):
        self.data.push(value)

    @property
    def accumulator(self) -> list:
        accum = self.peek()
        if not isinstance(accum, list):
            raise ParseError(f'Invalid parser state, expected=list, found={type(accum)}')
        return accum

    def push_state(self, delimiter: str|None = None) -> None:
        if delimiter is not None:
            self.expected_defn.push(delimiter)

    def pop_state(self, delimiter: str|None) -> None:
        if delimiter is None:
            return

        expected_def = self.expected_defn.peek()
        if self.expected_def != delimiter:
            raise ParseError(f'Invalid parser state, expected={expected_def}, found={delimiter}')
        self.expected_defn.pop()

    def push_exclusive_state(self, delimiter: str) -> None:
        if self.in_exclusive_def:
            raise ParseError('Invalid parser state, cannot next exclusive definition!')
        self.in_exclusive_def = True
        self.push_state(delimiter)

    def pop_exclusive_state(self, delimiter: str) -> None:
        if not self.in_exclusive_def:
            raise ParseError('Invalid parser state, not inside exclusive definition.')
        self.pop_state(delimiter)
        self.exclusive = False

    @contextmanager
    def in_string_mode(self):
        prev = self.mode
        self.mode = ParseMode.STRING
        yield self
        self.mode = prev

    @contextmanager
    def in_vocab(self, new_vocab):
        prev = self.vocab
        self.vocab = new_vocab
        yield self
        self.vocab = prev
