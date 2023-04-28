from dataclasses import InitVar, dataclass, field
from typing import Callable, ClassVar

from yak.vm.scanner import Scanner, Token
from yak.vm.value import Value


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


class ParseError(Exception):
    """Raised whenever an error is encountered during scanning."""


@dataclass
class Parser:
    vm: ...
    scanner: Scanner
    parsers: tuple[Callable] = field(init=False)
    EOF: ClassVar[str] = '#EOF#'

    def __post_init__(self):
        self.parsers = (self.parse_string, self.parse_number, self.parse_word)
        self.vm.push_value([])
        self.expected_delimiters = Stack()

    @property
    def current_accumulator(self) -> list[Value]:
        accum = self.vm.peek_value()
        if not isinstance(accum, list):
            msg = f'Invalid Parser State. expected=list, found={type(accum)}'
            raise ParseError(msg)
        return accum

    def parse(self) -> Value:
        while (value := self.next_value()) != Parser.EOF:
            if isinstance(value, WordRef) and value.parsing:
                continue
            self.current_accumulator.append(value)

        return self.current_accumulator

    def next_value(self) -> Value:
        if (token := self.scanner.scan_token()) is None:
            return Parser.EOF

        try:
            for parse in self.parsers:
                if (value := parse(token)) is not None:
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
