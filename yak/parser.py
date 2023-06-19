from contextlib import contextmanager
from enum import Enum

from yak.core import YakVal

# TODO refactor stack and import
# TODO implement the rest of the parser


@enum.unique
class ParseMode(Enum):
    PARSE = 'PARSE'
    STRING = 'STRING'


class Parser:
    EOF = '#EOF#'

    def __init__(self, runtime, scanner):
        self.runtime = runtime
        self.scanner = scanner
        self.in_exclusive_def = False
        self.mode = ParseMode.PARSE
        self.data = Stack()
        self.expected_defn = Stack
        self.vocab = None
        self.push([])

    def peek(self):
        return self.data.peek()

    def pop(self):
        return self.data.pop()

    def push(self, value):
        self.data.push(value)

    @contextmanager
    def in_string_mode(self):
        prev = self.mode
        self.mode = ParseMode.STRING
        yield self
        self.mode = prev

    @contextmanager
    def in_vocab(self, new_vocab):
        prev = self.vocab
        self.vocab = new_vocab
        yield self
        self.vocab = prev
