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


class YakStackError(YakError):
    """Raised during a stack operation failure."""


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


@dataclass(frozen=True)
class WordRef(YakPrimitive):
    # TODO add support for word hash
    name: str
    vocab: str
    parsing: bool = False

    def __str__(self) -> str:
        return self.name


@dataclass
class Word(YakPrimitive):
    name: str
    vocabulary: str
    parsing: bool = False
    docstr: str = ''

    @property
    def primitive(self) -> bool:
        return isinstance(self, PrimitiveWord)

    @property
    def ref(self) -> WordRef:
        return WordRef(self.name, self.vocabulary, self.parsing)

    def eval(self, vm):
        raise NotImplementedError(f'{self.name} is not implemented.')

@dataclass
class PrimitiveWord(Word):
    defn: Callable|None = None


@dataclass
class CompoundWord(Word):
    defn: list[Word] = field(default_factory=list)


@dataclass
class Vocabulary:
    name: str
    defs: dict[str, Word] = field(default_factory=dict)
    dirty: bool = False

    @property
    def count(self) -> int:
        return len(self.defs)

    def store(self, word: Word):
        self.defs[word.name] = word
        self.dirty = True

    def fetch(self, name: str) -> Word:
        return self.defs.get(name)
        return word

    def list(self) -> list[Word]:
        return self.defs.values()


class Stack(deque, YakPrimitive):
    """Stack data structure. Mostly a wrapper around `collections.deque`."""
    name: str

    @property
    def count(self) -> int:
        """
        Return the number of elements the stack.
        :returns: number of elements in the stack.
        :rtype: int.
        """
        return len(self)

    def pop(self) -> Value:
        """
        Remove and return the value at the top of the stack.
        :returns: value at the top of the stack.
        :rtype: Any.
        :raises YakStackError if stack is empty.
        """
        self.check_available(1)
        return super().pop()

    def peek(self) -> Value:
        """
        Return the value at the top of the stack, without removing it.
        :returns: the value at the top of the stack.
        :rtype: Any.
        :raises YakStackError if stack is empty.
        """
        self.check_available(1)
        return self[-1]

    def push(self, value: Value):
        """
        Push `value` onto the stack.
        :param value: value to push onto the top of the stack.
        :type value: Any.
        """
        self.append(value)

    def push_all(self, values: list[Value]):
        """
        Push all `values` onto the stack.
        :param values: values to push.
        :type values: list[Any].
        """
        self.extend(values)

    def empty(self) -> bool:
        """
        Check if stack is empty.
        :returns: `True` if stack is empty, `False` otherwise.
        :rtype: bool.
        """
        return self.count() == 0

    def not_empty(self) -> bool:
        """
        Check if stack is not empty.
        :returns: `True` is stack is not empty, `False` otherwise.
        :rtype: bool.
        """
        return not self.empty()

    def clear(self):
        """Clear stack."""
        super().__init__()

    def check_available(self, count: int):
        """
        Check if there are `count` values in the array.
        :param count: the number of values to check for in the array.
        :type count: int.
        :raises YakStackError if the available values are fewer than count.
        """
        if count > self.count:
            err = f'Underflow: expected={count}, actual={self.count}'
            raise YakStackError(err)


Value = str | float | int | bool | None | YakPrimitive
