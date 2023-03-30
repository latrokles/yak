from dataclasses import dataclass

from yak.lang.primitives import Stack, Word, YakPrimitive, YakUndefinedError


@dataclass
class Task(YakPrimitive):
    vm: ...
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
        self.bootstrap()
        self.run()

    def boostrap(self):



    def fetch_word(self, name: str) -> Word:
        # TODO account for vocabulary loading order
        if (word := self.vm.fetch_word(name)) is None:
            raise YakUndefinedError(f'word={name} is not defined.')
        print(f'Found word -> {word}')
        return word
