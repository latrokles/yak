from __future__ import annotations

import os

from dataclasses import dataclass, field

from yak.codebase import Codebase
from yak.interpreter import Interpreter
from yak.primitives.vocabulary import Vocabulary, def_vocabulary
from yak.primitives.word import Word, WordRef
from yak.util import get_logger
from yak.vocab.bootstrap import BOOTSTRAP
from yak.vocab.combinators import COMBINATORS
from yak.vocab.io import IO
from yak.vocab.kernel import KERNEL
from yak.vocab.parse import PARSE
from yak.vocab.syntax import SYNTAX
from yak.vocab.words import WORDS

LOG = get_logger()


@dataclass
class YakVirtualMachine:
    running: bool = False
    codebase: Codebase = field(init=False)

    def __post_init__(self):
        self.codebase = Codebase()

    def init(self) -> int:
        self.bootstrap()
        self.run()
        return self.shut_down()

    def bootstrap(self) -> None:
        LOG.info('booting up...')
        self.init_builtins()
        self.running = True

    def init_builtins(self):
        LOG.info('initializing builtins...')
        self.codebase.put_vocab(BOOTSTRAP)
        self.codebase.put_vocab(COMBINATORS)
        self.codebase.put_vocab(IO)
        self.codebase.put_vocab(KERNEL)
        self.codebase.put_vocab(PARSE)
        self.codebase.put_vocab(SYNTAX)
        self.codebase.put_vocab(WORDS)

    def run(self) -> None:
        bootstrap_word = self.fetch_word('bootstrap')
        LOG.info(self.codebase)
        Interpreter(self).init(bootstrap_word)

    def shut_down(self) -> int:
        LOG.info('shutting down...')
        return 0

    def vocab_defined(self, vocab_name: str) -> bool:
        return self.codebase.has_vocab(vocab_name)

    def new_vocab(self, vocab_name: str) -> bool:
        LOG.info(f'defining new vocabulary: {vocab_name}')
        self.codebase.put_vocab(def_vocabulary(vocab_name))

    def fetch_word(self, ref: WordRef|str, vocabulary_name: str|None = None) -> Word|None:
        # TODO do this right...
        # requires vocabulary parsing, which requires parse words.
        for vocab in self.codebase.vocabularies.values():
            if (word := vocab.fetch(str(ref))) is not None:
                return word
        return None

    def store_word(self, word: Word):
        self.codebase.put_word(word)
