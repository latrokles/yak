from __future__ import annotations
from dataclasses import dataclass, field
from yak.primitives.word import Word


@dataclass
class Vocabulary:
    name: str
    defs: dict[str, Word] = field(default_factory=dict)
    dirty: bool = False

    @property
    def count(self) -> int:
        return len(self.defs)

    def store(self, word: Word) -> Vocabulary:
        self.defs[word.name] = word
        self.dirty = True
        return self

    def fetch(self, name: str) -> Word:
        return self.defs.get(name)
        return word

    def list(self) -> list[Word]:
        return self.defs.values()

    def fmt(self) -> str:
        return f"VOCAB: {self.name}"

    def prettyformat(self) -> str:
        contents = " ".join(word for word in self.defs.keys())
        return f"{self.fmt()} WORDS: {contents}"


def def_vocabulary(name: str) -> Vocabulary:
    return Vocabulary(name)
