from dataclasses import dataclass, field
from enum import Enum
from typing import Callable, ClassVar

from yak.lang.parse import Parser, Scanner, Token
from yak.lang.primitives import Value, Word, WordRef, YakError
from yak.lang.primitives.numbers import is_int, is_float


class YakParseError(YakError):
    """Raised if the parser enters an invalid state."""


class ParseMode(Enum):
    PARSE = 'PARSE'
    RAW = 'RAW'


@dataclass
class YakParser(Parser):
    task: ...
    scanner: Scanner
    mode: ParseMode = ParseMode.PARSE
    parsers: tuple[Callable] = field(init=False)
    EOF: ClassVar[str] = '#EOF#'

    def __post_init__(self):
        self.parsers = (self.parse_string, self.parse_number, self.parse_word)
        self.push_state([])

    @property
    def current_state(self) -> list[Value]:
        accum = self.task.datastack.peek()
        if not isinstance(accum, list):
            msg = f'Invalid Parser State. expected=list, found={type(accum)}'
            raise YakParseError(msg)
        return accum

    def push_state(self, quote: list[Value]) -> None:
        self.task.datastack.push(quote)

    def parse(self) -> Value:
        while (value := self.next_value()) != YakParser.EOF:
            self.current_state.append(value)
        return self.current_state

    def next_value(self) -> Value:
        if (token := self.scanner.scan_token()) is None:
            return YakParser.EOF

        try:
            for parse in self.parsers:

                if (value := parse(token)) is not None:
                    # TODO find a better way to handle this
                    if isinstance(value, WordRef) and value.parsing:
                        continue
                    return value

            raise YakParseError(f'Unknown token={token}')
        except Exception as e:
            raise YakParseError(f'Unable to parse value error={e}')

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
            word = self.task.fetch_word(token.text)
            if word.parsing:
                word.eval(self.task)
            return word.ref
        except Exception as e:
            raise YakParseError(f'Unable to parse word: {e}')
