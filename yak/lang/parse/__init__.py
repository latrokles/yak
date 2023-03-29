from __future__ import annotations
from dataclasses import dataclass
from typing import Protocol

from yak.lang.primitives import Symbol, Value, Word, YakPrimitive


@dataclass
class Token(YakPrimitive):
    text: str
    col_start: int
    col_end: int
    row: int


class Scanner:
    def scan_token(self) -> Token|None:
        pass


class Parser:
    def parse(self) -> list[Value]:
        pass

    def parse_string(self, token: Token) -> str|None:
        pass

    def parse_number(self, token: Token) -> float|int|None:
        pass

    def parse_symbol(self, token: Token) -> Symbol|None:
        pass

    def parse_word(self, token: Token) -> Word|Symbol:
        pass

    def raw(self) -> Parser:
        pass

    def push_definition(self, sym: Symbol) -> None:
        pass

    def pop_definition(self, sym: Symbol) -> None:
        pass

    def push_exclusive_definition(self, sym: Symbol) -> None:
        pass

    def pop_exclusive_definition(self, sym: Symbol) -> None:
        pass

