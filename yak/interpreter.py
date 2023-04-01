from dataclasses import dataclass

from yak.primitives import Value, YakError, YakUndefinedError
from yak.primitives.quotation import Quotation
from yak.primitives.stack import Stack
from yak.primitives.word import Word, WordRef


@dataclass
class Interpreter:
    vm: ...
    active: bool = False
    callframe: Quotation|None = None
    datastack: Stack|None = None
    callstack: Stack|None = None
    errorstack: Stack|None = None
    retainstack: Stack|None = None

    def __post_init__(self):
        self.datastack = (self.datastack or Stack('data'))
        self.callstack = (self.callstack or Stack('call'))
        self.errorstack = (self.errorstack or Stack('error'))
        self.retainstack = (self.retainstack or Stack('retain'))

    def init(self, word: Word) -> None:
        self.datastack.push(self.get_init_defn(word))
        self.call()

    def get_init_defn(self, word: Word) -> Quotation:
        if word.primitive:
            return Quotation([word.ref])
        return word.defn

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
        while self.active:
            try:
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
                if self.handle_error(e):
                    return

        self.callframe = None

    def eval(self, value: Value) -> None:
        if not isinstance(value, WordRef):
            self.datastack.push(value)
            return

        self.execute(self, value)

    def execute(self, word_ref: WordRef) -> None:
        try:
            word = self.fetch_word(word_ref.name, word_ref.vocab)
            word.eval(self)
        except Exception as e:
            self.callstack.push(self.callframe)
            raise

    def handle_error(self, err: Exception) -> bool:
        if not self.active:
            traceback.print_exc()
            self.reset()
            return True

        self.datastack.push(err)
        try:
            throw = self.fetch_word('throw', 'errors')
            self.eval(throw)
            return False
        except Exception as e:
            print(f'There was an error executing `throw`, error={e}')
            traceback.print_exc()
            self.reset()
            return True

    def fetch_word(self, name: str, vocab: str|None = None) -> Word:
        if vocab is not None:
            if (word := self.vm.fetch_word(name, vocab)) is None:
                raise YakUndefinedError(f'word={name} is not defined in vocabulary={vocab}.')
            return word

        # TODO account for vocabulary loading order resolution.
        if (word := self.vm.fetch_word(name)) is None:
            raise YakUndefinedError(f'word={name} is not defined.')
        print(f'Found word -> {word}')
        return word

    def reset(self) -> None:
        self.callstack.clear()
        self.datastack.clear()
        self.errorstack.clear()
        self.retainstack.clear()
        self.callframe = None
