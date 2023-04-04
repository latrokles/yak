from __future__ import annotations

import os

from dataclasses import dataclass, field

from yak.interpreter import Interpreter
from yak.primitives.vocabulary import Vocabulary, def_vocabulary
from yak.primitives.word import Word, WordRef
from yak.util import get_logger

LOG = get_logger()


@dataclass
class YakOS:
    running: bool = False

    def init(self) -> int:
        self.bootstrap()
        self.run()
        return self.shut_down()

    def bootstrap(self) -> None:
        LOG.info('booting up...')
        self.running = True

    def run(self) -> None:
        # TODO pass vm when we have io devices
        Interpreter().init().start()

    def shut_down(self) -> int:
        LOG.info('shutting down...')
        return 0
