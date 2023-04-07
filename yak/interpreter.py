from __future__ import annotations
from dataclasses import dataclass
from traceback import print_exc

from yak.codebase import Codebase
from yak.primitives import Value, YakError, YakUndefinedError, print_object
from yak.primitives import Value
from yak.primitives.quotation import Quotation
from yak.primitives.namespace import Namespace
from yak.primitives.stack import Stack
from yak.primitives.vocabulary import Vocabulary, def_vocabulary
from yak.primitives.word import Word, WordRef
from yak.util import get_logger
from yak.vocab.bootstrap import BOOTSTRAP
from yak.vocab.parse import PARSE
from yak.vocab.quotations import QUOTATIONS
from yak.vocab.syntax import SYNTAX
from yak.vocab.words import WORDS

LOG = get_logger()

BUILTINS = [
    BOOTSTRAP,
    PARSE,
    QUOTATIONS,
    SYNTAX,
    WORDS,
]


@dataclass
class Interpreter:
    active: bool = False
    current_vocab: str|None = None
    codebase: Codebase|None = None

    callframe: Quotation|None = None
    loaded_vocabs: Stack|None = None

    datastack: Stack|None = None
    callstack: Stack|None = None
    errorstack: Stack|None = None
    retainstack: Stack|None = None
    namestack: Stack|None = None
    GLOBAL: Namespace|None = None

    def __post_init__(self):
        self.codebase = (self.codebase or Codebase())
        self.loaded_vocabs = (self.loaded_vocabs or Stack())
        self.datastack = (self.datastack or Stack())
        self.callstack = (self.callstack or Stack())
        self.errorstack = (self.errorstack or Stack())
        self.retainstack = (self.retainstack or Stack())
        self.namestack = (self.namestack or Stack())
        self.GLOBAL = (self.GLOBAL or Namespace('global'))

    def init(self) -> Interpreter:
        self.namestack.push(self.GLOBAL)
        self.init_codebase()
        self.set_global('*interpreter*', self)
        return self

    def init_codebase(self):
        LOG.info('initializing builtins...')
        for vocab in BUILTINS:
            self.load_vocab(vocab)

    def load_vocab(self, vocab: Vocabulary):
        self.codebase.put_vocab(vocab)
        self.use(vocab.name)

    def use(self, vocab: str):
        self.loaded_vocabs.push(vocab)

    def start(self, word: Word|None = None) -> None:
        LOG.info(f'initializing interpreter with word: {word}')
        self.datastack.push(self.get_init_defn(word))
        self.call()
        self.run()

    def get_init_defn(self, word: Word|None) -> Quotation:
        if word is None:
            word = self.fetch_word('bootstrap')

        if word.primitive:
            return Quotation([word.ref])

        return word.defn

    def global_namespace(self) -> Namespace:
        return self.GLOBAL

    def get_variable(self, name: str) -> Value|None:
        for namespace in self.namestack.from_the_top():
            if namespace.has_binding(name):
                return namespace.get_binding(name)
        return None

    def set_variable(self, var: str, val: Value):
        self.namestack.peek().set_binding(var, val)

    def get_global(self, var: str) -> Value:
        return self.GLOBAL.get_binding(var)

    def set_global(self, var: str, val: Value):
        self.GLOBAL.set_binding(var, val)

    def set_current_vocabulary(self, vocab_name: str):
        LOG.info(f'switching to vocab: {vocab_name}')
        if not self.codebase.has_vocab(vocab_name):
            LOG.info(f'vocabulary not defined: {vocab_name}')
            self.codebase.new_vocab(vocab_name)

        self.current_vocab = vocab_name
        if vocab_name not in self.loaded_vocabs:
            self.loaded_vocabs.push(vocab_name)

    def call(self) -> None:
        """
        Get the quotation on top of the datastack and set it as the current
        callframe so that it can be executed.

        If there is a quotation in the current callframe, push it onto the
        callstack so that it can be resumed later.

        :raises YakError: if the value on top of the stack is not a Quotation.
        """
        quote = self.datastack.peek()
        if not isinstance(quote, Quotation):
            raise YakError(f'`call` expected `quot`, but got {type(quote)}')

        if (self.callframe is not None) and (not self.callframe.empty):
            self.callstack.push(self.callframe)

        self.callframe = self.datastack.pop()

    def run(self) -> None:
        """
        Advance through the values in the callframe the quotation and evaluate
        them.

        If the callframe is None, we look for a quotation in the callstack to
        execute and if None is found we've reached the end of the interpreter's word.

        If the callframe is empty, we've reached the end of the interpreter's word.
        """
        self.active = True
        while self.active:
            try:
                LOG.info(f'datastack: {print_object(Quotation(self.datastack))}')
                LOG.info(f'callframe: {print_object(self.callframe)}')
                if self.callframe is None or self.callframe.empty:
                    if self.callstack.empty():
                        break

                    self.callframe = self.callstack.pop()
                    continue

                # get first element to eval and advance position on callframe
                to_evaluate = self.callframe.head
                self.callframe = self.callframe.tail
                self.eval(to_evaluate)
            except Exception as e:
                LOG.error(f'Something went wrong: {e}')
                if self.handle_error(e):
                    return

        self.callframe = None

    def eval(self, value: Value) -> None:
        if not isinstance(value, WordRef):
            self.datastack.push(value)
            return

        self.execute(value)

    def execute(self, word_ref: WordRef) -> None:
        try:
            word = self.fetch_word(word_ref.name, word_ref.vocab)
            word.eval(self)
        except Exception as e:
            self.callstack.push(self.callframe)
            raise

    def handle_error(self, err: Exception) -> bool:
        if not self.active:
            print_exc()
            self.reset()
            return True

        self.datastack.push(err)
        try:
            throw = self.fetch_word('throw', 'errors')
            self.eval(throw)
            return False
        except Exception as e:
            print(f'There was an error executing `throw`, error={e}')
            print_exc()
            self.reset()
            return True

    def fetch_word(self, name: str, vocab: str|None = None) -> Word:
        if vocab is not None:
            if (word := self.codebase.get_word(name, vocab)) is None:
                raise YakUndefinedError(f'word={name} is not defined in vocabulary={vocab}.')
            return word

        if self.current_vocab is not None:
            if (word := self.codebase.get_word(name, self.current_vocab)) is not None:
                return word

        for vocab_name in self.loaded_vocabs.from_the_top():
            LOG.info(f'searching for `{name}` in `{vocab_name}`')
            if (word := self.codebase.get_word(name, vocab_name)) is not None:
                return word

        raise YakUndefinedError(f'word={name} is not defined.')

    def store_word(self, word: Word):
        self.codebase.put_word(word)

    def reset(self) -> None:
        self.callstack.clear()
        self.datastack.clear()
        self.errorstack.clear()
        self.retainstack.clear()
        self.callframe = None
