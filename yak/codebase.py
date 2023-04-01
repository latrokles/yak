from __future__ import annotations
from dataclasses import dataclass, field

from yak.primitives import YakUndefinedError


@dataclass
class Codebase:
    vocabularies: dict[str, Vocabulary] = field(default_factory=dict)

    def put_vocab(self, vocab: Vocabulary) -> Codebase:
        self.vocabularies[vocab.name] = vocab
        return self

    def get_vocab(self, name: str) -> Codebase:
        if (vocab := self.vocabularies.get(name)) is None:
            raise YakUndefinedError(f'There is no vocabulary with name={vocab_name}')
        return vocab

    def put_word(self, word: Word) -> None:
        self.get_vocab(word.vocabulary).store(word)

    def get_word(self, ref: WordRef|str, vocab_name: str) -> Word|None:
        return self.get_vocab(vocab_name).fetch(str(ref))
