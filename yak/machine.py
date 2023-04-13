from __future__ import annotations

import gnureadline as readline
import sys

from dataclasses import dataclass, field

from yak.interpreter import Interpreter
from yak.util import HISTORY, get_logger


@dataclass
class YakMachine:
    port: int
    debug: bool = False
    running: bool = False
    imagepath: str|None = None
    scriptpath: str|None = None
    logger: logging.Logger = field(init=False)

    def __post_init__(self):
        loglevel = 'DEBUG' if self.debug else 'INFO'
        self.logger = get_logger(loglevel)

    def with_image(self, pathname: str|None = None) -> YakMachine:
        raise NotImplementedError()

    def with_script(self, pathname: str|None = None) -> YakMachine:
        if pathname is not None:
            self.scriptpath = pathname
        return self

    def boot(self) -> int:
        try:
            self.logger.info(f'starting yak: {self}')
            self.read_history()
            self.running = True
            exit_code = self.run()
            self.logger.info('stopping yak')
            sys.exit(exit_code)
        finally:
            self.write_history()

    def run(self) -> int:
        Interpreter(self.logger).init().start()
        return 0

    def stop(self):
        self.running = False


@dataclass
class GraphicYakMachine(YakMachine):
    def with_image(self, pathname: str|None = None) -> YakMachine:
        self.imagepath = (pathname or 'images/default-graphics.image')
        return self

    def read_history(self):
        pass

    def write_history(self):
        pass


@dataclass
class ConsoleYakMachine(YakMachine):
    def with_image(self, pathname: str|None = None) -> YakMachine:
        self.imagepath = (pathname or 'images/default-minimal.image')
        return self

    def read_history(self):
        readline.read_history_file(HISTORY)
        readline.set_history_length(-1)

    def write_history(self):
        readline.write_history_file(HISTORY)
