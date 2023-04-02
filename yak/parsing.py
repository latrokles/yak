from __future__ import annotations
from dataclasses import InitVar, dataclass, field
from enum import Enum
from io import StringIO
from typing import Callable, ClassVar

from yak.primitives import Value, YakError, YakPrimitive
from yak.primitives.numbers import is_int, is_float
from yak.primitives.quotation import Quotation
from yak.primitives.strings import blank
from yak.primitives.word import Word, WordRef


class ScanError(YakError):
    """Raised whenever an error is encountered during scanning."""


@dataclass
class Token(YakPrimitive):
    text: str
    col_start: int
    col_end: int
    row: int


@dataclass
class Scanner:
    """
    The Scanner consumes source text and splits it into space delimited tokens.
    """

    src_txt: InitVar[str]
    src: StringIO = field(init=False)
    src_len: int = field(init=False)

    row: int = 0
    col: int = 0
    pos: int = 0

    def __post_init__(self, src_txt: str):
        """Initialize source stream."""
        self.src = StringIO(src_txt)
        self.src_len = len(src_txt)

    def scan_token(self) -> Token|None:
        """
        Consume and return the next token in the stream.

        :returns: the next token in the stream.
        :rtype: Token.

        :raises YakScanError: when the token cannot be scanned correctly.
        """
        if self.pos == self.src_len:
            return None

        token_chars = []
        char = self.scan_char()

        while blank(char):
            char = self.scan_char()

        start = self.col
        if char == '"':
            return self.scan_string()

        while not blank(char):
            token_chars.append(char)
            char = self.scan_char()
        stop = self.col
        return Token(''.join(token_chars), start, stop, self.row)

    def scan_char(self) -> str:
        """
        Consume and return the next character in the stream.

        :returns: the next character in the stream.
        :rtype: str.
        """
        if self.pos == self.src_len:
            return ''

        char = self.src.read(1)
        self.pos += 1
        self.col += 1

        if self.src.getvalue()[self.pos - 1] == '\n':
            self.col = 0
            self.row += 1

        return char

    def scan_string(self) -> Token:
        """
        Consume characters until the closing `"` in the stream and return the
        enclosed string as a token.

        :returns: the token containing the scanned string.
        :rtype: Token.
        """
        token_chars = ['"']
        start = self.col
        char = self.scan_char()

        while char != '"' and self.pos < self.src_len:
            token_chars.append(char)
            char = self.scan_char()

        # consume the closing quote
        token_chars.append(char)
        stop = self.col
        text = ''.join(token_chars)

        if char != '"':
            message = f'Unterminated string. value={text}'
            raise ScanError(f'{message}, line={self.row}, pos=[{start}:{stop}]')
        return Token(text, start, stop, self.row)


class ParseError(YakError):
    """Raised if the parser enters an invalid state."""


class ParseMode(Enum):
    PARSE = 'PARSE'
    RAW = 'RAW'


@dataclass
class Parser:
    interpreter: ...
    scanner: Scanner
    mode: ParseMode = ParseMode.PARSE
    parsers: tuple[Callable] = field(init=False)
    EOF: ClassVar[str] = '#EOF#'

    def __post_init__(self):
        self.parsers = (self.parse_string, self.parse_number, self.parse_word)
        self.push_state(Quotation())

    @property
    def current_state(self) -> list[Value]:
        accum = self.interpreter.datastack.peek()
        if not isinstance(accum, Quotation):
            msg = f'Invalid Parser State. expected=Quotation, found={type(accum)}'
            raise ParseError(msg)
        return accum

    def push_state(self, quote: Quotation) -> None:
        self.interpreter.datastack.push(quote)

    def parse(self) -> Value:
        while (value := self.next_value()) != Parser.EOF:
            self.current_state.append(value)
        return self.current_state

    def next_value(self) -> Value:
        if (token := self.scanner.scan_token()) is None:
            return Parser.EOF

        try:
            for parse in self.parsers:

                if (value := parse(token)) is not None:
                    # TODO find a better way to handle this
                    if isinstance(value, WordRef) and value.parsing:
                        continue
                    return value

            raise ParseError(f'Unknown token={token}')
        except Exception as e:
            raise ParseError(f'Unable to parse value error={e}')

    def parse_string(self, token: Token) -> str|None:
        if token.text.startswith('"') and token.text.endswith('"'):
            return token.text[1:-1]
        return None

    def parse_number(self, token: Token) -> float|int|None:
        if is_int(token.text):
            return int(token.text)

        if is_float(token.text):
            return float(token.text)

        return None

    def parse_word(self, token: Token) -> WordRef|None:
        try:
            word = self.interpreter.fetch_word(token.text)
            if word.parsing:
                word.eval(self.interpreter)
            return word.ref
        except Exception as e:
            raise ParseError(f'Unable to parse word: {e}')
