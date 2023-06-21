from __future__ import annotations
from dataclasses import dataclass
from traceback import print_exc

from yak.yak.core import Stack


@dataclass
class CallFrame:
    code: list = field(default_factory=list)
    ip: int = 0

    def next(self) -> Value:
        if self.ip >= self.code.count():
            raise RuntimeError("no more code to evaluate in callframe!")

        value = self.code[self.ip]
        self.ip += 1
        return value

    def empty(self) -> bool:
        return len(self.code) != 0


@dataclass
class NullCallFrame(CallFrame):
    def empty(self) -> bool:
        return True


@dataclass
class Interpreter:
    active: bool = False
    callframe: CallFrame = field(default_factory=NullCallFrame)

    datastack: Stack = field(default_factory=Stack())
    retainstack: Stack = field(default_factory=Stack())
    callstack: Stack = field(default_factory=Stack())

    def initialize(self):
        pass

    def push(self, val: Value):
        self.datastack.push(val)

    def pop(self) -> Value:
        return self.datastack.pop()

    def peek(self) -> Value:
        return self.datastack.peek()

    def call(self) -> None:
        """
        Get the quotation from top of the datastack and set it as the current
        callframe so that it can be executed.

        If there is a valid callframe set, push it onto the callstack so that
        it can be resumed later.

        :raises YakError: if the value on top of the stack is not a Quotation.
        """
        quote = self.peek()
        if not isinstance(quote, Quotation):
            raise YakError(f'`call` expected `quot`, but got `{type(quote)}`')

        if not self.callframe.empty():
            self.callstack.push(self.callframe)

        self.callframe = CallFrame(self.datastack.pop())

    def run(self) -> None:
        """
        Advance through the values in the callframe's code and evaluate them.

        If the callframe is empty/null we look for a quotation in the callstack
        to execute if none is found, we've reached the of the interpreter's
        word.
        """
        self.active = True
        while self.active:
            try:
                if self.callframe.empty():
                    if self.callstack.empty():
                        break

                    self.callframe = self.callstack.pop()
                    continue

                # get next element to evaluate in the callframe
                evaluate_next = self.callframe.next()
                self.eval(evaluate_next)
            except Exception as e:
                if self.handle_error(e):
                    return
        self.callframe = NullCallFrame()

    def eval(self, value: Value) -> None:
        if not isinstance(value, WordPointer):
            self.datastack.push(value)
            return
        self.execute(value)

    def execute(self, word_ptr: WordPointer) -> None:
        try:
            word = self.get_word(word_ptr)
            word.exec(self)
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
            throw = self.get_word_in_vocab('throw', 'errors')
            self.eval(throw)
            return False
        except Exception as e:
            print(f'There was an error executing `throw`, error={e}')
            print_exc()
            self.reset()
            return True
