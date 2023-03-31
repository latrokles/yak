from dataclasses import dataclass

from yak.lang.primitives import Stack, Value, Word, WordRef, YakError, YakPrimitive, YakUndefinedError
from yak.lang.primitives.quotation import Quotation


@dataclass
class Task(YakPrimitive):
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

    def start(self, word: Word) -> int:
        self.run()

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
        execute and if None is found we've reached the end of the task's word.

        If the callframe is empty, we've reached the end of the task's word.
        """
        while self.active:
            try:
                if self.callframe is None:
                    if self.callstack.empty():
                        break

                    self.callframe = self.callstack.pop()
                    continue

                if self.callframe.empty:
                    break

                # get first element to eval and advance position on callframe
                to_evaluate = self.callframe.head
                self.callframe = self.callframe.tail
                self.eval(to_evaluate)
            except Exception as e:
                if self.handle_error(e):
                    return

        self.callframe = None

    def eval(self, value: Value) -> None:
        pass

    def handle_error(self, err: Exception) -> bool:
        pass





    def fetch_word(self, name: str) -> Word:
        # TODO account for vocabulary loading order
        if (word := self.vm.fetch_word(name)) is None:
            raise YakUndefinedError(f'word={name} is not defined.')
        print(f'Found word -> {word}')
        return word
