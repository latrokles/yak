from dataclasses import dataclass, field
from typing import Callable

from yak.primitives import Value, YakPrimitive


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


def define_compound(vocabulary_name: str,
                    name: str,
                    defn: list[Value],
                    parse: bool = False) -> Word:
    # TODO add docs
    return CompoundWord(name, vocabulary_name, parse, 'nodoc', defn)


def define_primitive(vocabulary_name: str,
                     name: str,
                     defn: Callable,
                     parse: bool = False) -> Word:
    return PrimitiveWord(name, vocabulary_name, parse, defn.__doc__, defn)
