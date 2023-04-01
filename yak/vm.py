from __future__ import annotations

import os

from dataclasses import dataclass, field

from yak.codebase import Codebase
from yak.interpreter import Interpreter
from yak.primitives import Vocabulary, Word, WordRef
from yak.primitives.bootstrap import BOOTSTRAP
from yak.primitives.combinators import COMBINATORS
from yak.primitives.kernel import KERNEL
from yak.primitives.io import IO
from yak.primitives.parsing import PARSING
from yak.primitives.syntax import SYNTAX
from yak.util import LOG


@dataclass
class YakVirtualMachine:
    running: bool = False
    codebase: Codebase = field(init=False)

    def __post_init__(self):
        self.codebase = Codebase()

    def start(self) -> int:
        self.init()
        self.run()
        return self.shut_down()

    def init(self) -> None:
        LOG.info('booting up...')
        self.init_builtins()
        self.bootstrap()
        self.run()

    def init_builtins(self):
        LOG.info('initializing builtins...')
        self.codebase.put_vocab(BOOTSTRAP)
        self.codebase.put_vocab(COMBINATORS)
        self.codebase.put_vocab(IO)
        self.codebase.put_vocab(KERNEL)
        self.codebase.put_vocab(PARSING)
        self.codebase.put_vocab(SYNTAX)

    def bootstrap(self) -> None:
        self.running = True
        pass

    def run(self) -> None:
        iter_count = int(os.getenv('ITERCOUNT', '5'))
        for i in range(iter_count):
            LOG.info(f'executing: {i}!')

    def shut_down(self) -> int:
        LOG.info('shutting down...')
        return 0


    def fetch_word(self, ref: WordRef|str, vocabulary_name: str|None = None) -> Word|None:
        # TODO do this right...
        # requires vocabulary parsing, which requires parse words.
        word = None
        for vocab in self.codebase.vocabularies.values():
            if (word := vocab.fetch(str(ref))) is None:
                continue
        return word
