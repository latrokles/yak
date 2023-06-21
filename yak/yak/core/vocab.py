from __future__ import annotations
from dataclasses import dataclass, field

from .values import YakPrimitive

@dataclass
class Vocabulary(YakPrimitive):
    name: str
    defs: dict[str, Word] = field(default_factory=dict)

    @property
    def count(self) -> int:
        return len(self.defs)

    def put(self, word: Word) -> Vocabulary:
        self.defs[word.name] = word
        return self

    def get(self, name: str) -> Word|None:
        return self.defs.get(name)

    def list(self) -> list[Word]:
        return self.defs.values()

    def fmt(self) -> str:
        return f"<VOCAB: {self.name}>"
