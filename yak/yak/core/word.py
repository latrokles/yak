from __future__ import annotations
from dataclasses import dataclass, field
from typing import Callable

from .values import YakPrimitive, YakVal


@dataclass(frozen=True)
class WordRef(YakPrimitive):
    name: str
    vocabulary: str
    parsing: bool = False

    def __str__(self) -> str:
        return self.name

    def fmt(self) -> str:
        return self.name


@dataclass
class Word(YakPrimitive):
    name: str
    vocabulary: str
    parsing: bool = False
    ref: WordRef = field(init=False)

    def __post_init__(self):
        self.ref = WordRef(self.name, self.vocabulary, self.parsing)

    @property
    def primitive(self) -> bool:
        return isinstance(self, PrimitiveWord)

    def fmt(self) -> str:
        return self.name


@dataclass
class PrimitiveWord(Word):
    defn: Callable|None = None

    # TODO find a better name for runtime and give it a protocol of some sort.
    def eval(self, runtime):
        self.defn(runtime)


@dataclass
class CompoundWord(Word):
    defn: list[YakVal] = field(default_factory=list)

    # TODO handle compound parse words (this may be trickier than expected).
    def eval(self, runtime):
        runtime.push(self.defn)
        runtime.call()


def def_primitive(vocab: str, name: str, defn: Callable, parse: bool = False) -> Word:
    return PrimitiveWord(name, vocab, parse, defn)


def def_compound(vocab: str, name: str, defn: list[YakVal], parse: bool = False) -> Word:
    return CompoundWord(name, vocab, parse, defn)
