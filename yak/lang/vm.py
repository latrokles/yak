from __future__ import annotations

import os

from dataclasses import dataclass, field

from yak.lang.primitives import Vocabulary, Word, WordRef
from yak.lang.primitives.task import Task
from yak.lang.primitives.syntax import SYNTAX
from yak.util import LOG


@dataclass
class YakVirtualMachine:
    tasks: list[Task] = field(default_factory=list)
    vocabularies: dict[str, Vocabulary] = field(default_factory=dict)

    def run(self) -> int:
        try:
            self.boot_up()
            self.execute_loop()
            return self.shut_down()
        except Exception as e:
            LOG.critical(f'wtf?: {e}')
            return -1

    def boot_up(self) -> None:
        LOG.info('booting up...')
        self.init_builtins()

    def execute_loop(self) -> None:
        iter_count = int(os.getenv('ITERCOUNT', '5'))
        for i in range(iter_count):
            LOG.info(f'executing: {i}!')

    def shut_down(self) -> int:
        LOG.info('shutting down...')
        return 0

    def init_builtins(self):
        LOG.info('initializing builtins...')
        self.vocabularies[SYNTAX.name] = SYNTAX

    def fetch_word(self, ref: WordRef|str, vocabulary_name: str|None = None) -> Word|None:
        # TODO implement vocabulary lookup
        word = None
        for vocab in self.vocabularies.values():
            if (word := vocab.fetch(str(ref))) is None:
                continue
        return word
