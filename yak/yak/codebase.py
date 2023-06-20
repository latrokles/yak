from __future__ import annotations
from dataclasses import dataclass, field
from logging import Logger

from yak.primitives import YakUndefinedError
from yak.primitives.vocabulary import Vocabulary, def_vocabulary



@dataclass
class Codebase:
    logger: logging.Logger
    vocabularies: dict[str, Vocabulary] = field(default_factory=dict)

    def new_vocab(self, vocab_name: str):
        self.logger.info(f'defining new vocabulary: {vocab_name}')
        self.put_vocab(def_vocabulary(vocab_name))

    def has_vocab(self, vocab_name: str) -> bool:
        return vocab_name in self.vocabularies.keys()

    def put_vocab(self, vocab: Vocabulary) -> Codebase:
        self.logger.info(f'loading vocabulary: {vocab.name}')
        self.vocabularies[vocab.name] = vocab
        return self

    def get_vocab(self, name: str) -> Codebase:
        if (vocab := self.vocabularies.get(name)) is None:
            raise YakUndefinedError(f'There is no vocabulary with name={name}')
        return vocab

    def put_word(self, word: Word) -> None:
        self.get_vocab(word.vocabulary).store(word)

    def get_word(self, ref: WordRef|str, vocab_name: str) -> Word|None:
        return self.get_vocab(vocab_name).fetch(str(ref))

    def __str__(self) -> str:
        vocabs = ' '.join(self.vocabularies.keys())
        return f'vocabularies: {vocabs}'
