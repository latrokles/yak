from dataclasses import dataclass, field
from typing import Callable

from yak.primitives import Value, YakPrimitive
from yak.primitives.quotation import Quotation


@dataclass(frozen=True)
class WordRef(YakPrimitive):
    # TODO add support for word hash
    name: str
    vocab: str
    parsing: bool = False

    def __str__(self) -> str:
        return self.name

    def print_object(self) -> str:
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

    def eval(self, interpreter):
        self.defn(interpreter)


@dataclass
class CompoundWord(Word):
    defn: Quotation[Value] = field(default_factory=list)

    def eval(self, interpreter):
        if self.parsing:
            self.exec(interpreter)
            return

        interpreter.datastack.push(self.defn)
        interpreter.call()

    def exec(self, interpreter):
        for val in self.defn:
            interpreter.eval(val)


def def_compound(vocabulary_name: str,
                 name: str,
                 defn: Quotation[Value],
                 parse: bool = False) -> Word:
    # TODO add docs
    return CompoundWord(name, vocabulary_name, parse, 'nodoc', defn)


def def_primitive(vocabulary_name: str,
                  name: str,
                  defn: Callable,
                  parse: bool = False) -> Word:
    return PrimitiveWord(name, vocabulary_name, parse, defn.__doc__, defn)
