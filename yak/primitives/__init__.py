from __future__ import annotations

from collections import deque
from dataclasses import dataclass, field
from typing import Callable, ClassVar


class YakPrimitive:
    def fmt(self) -> str:
        return str(self)

    def prettyformat(self) -> str:
        return repr(self)


class YakError(Exception, YakPrimitive):
    """The top level Yak error."""


class YakUndefinedError(YakError):
    """Raised when a word is undefined."""


def prettyformat(value: Value) -> str:
    if value is None:
        return fmt(value)

    match value:
        case bool():
            return fmt(value)
        case str():
            return repr(value).replace("'", '"')
        case YakPrimitive():
            return value.prettyformat()
        case _:
            return repr(value)


def fmt(value: Value) -> str:
    if value is None:
        return 'nil'

    match value:
        case bool():
            return str(value)[0].lower()
        case str():
            return value
        case YakPrimitive():
            return value.fmt()
        case _:
            return str(value)



@dataclass(frozen=True)
class Symbol(YakPrimitive):
    value: str
    _instances: ClassVar[dict[str, Symbol]] = {}

    @classmethod
    def make(cls, value: str) -> Symbol:
        sym = cls._instances.get(value)
        if sym is None:
            sym = cls(value)
            cls._instances[value] = sym
        return sym


Value = str | float | int | bool | None | YakPrimitive
