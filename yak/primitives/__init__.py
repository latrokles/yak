from __future__ import annotations

from collections import deque
from dataclasses import dataclass, field
from typing import Callable, ClassVar


class YakPrimitive:
    def print_object(self) -> str:
        return repr(self)


class YakError(Exception, YakPrimitive):
    """The top level Yak error."""


class YakUndefinedError(YakError):
    """Raised when a word is undefined."""


def print_object(value: Value) -> str:
    if value is None:
        return 'nil'

    match value:
        case bool():
            return repr(value)[0].lower()
        case YakPrimitive():
            return value.print_object()
        case _:
            return repr(value)


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
