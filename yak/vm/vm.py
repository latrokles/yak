from dataclasses import dataclass, field
from enum import Enum
from typing import Any

from yak.vm.chunk import Chunk
from yak.vm.opcode import Opcode
from yak.vm.value import Value, print_value


class VMError(Exception):
    """Raised whenever there is a VM execution error."""


@dataclass
class Closure:
    pass


@dataclass
class CallFrame:
    pass


class InterpretResult(Enum):
    INTERPRET_OK = 0x00
    INTERPRET_COMPILE_ERROR = 0x01
    INTERPRET_RUNTIME_ERROR = 0x10



@dataclass
class VirtualMachine:
    chunk: Chunk|None = None
    ip: int = 0

    d_stack: list[Any] = field(default_factory=list)
    c_stack: list[CallFrame] = field(default_factory=list)

    def get_value(self, index: int) -> Any:
        return self.d_stack[index]

    def peek_value(self) -> Any:
        return self.d_stack[-1]

    def pop_value(self) -> Any:
        return self.d_stack.pop()

    def push_value(self, value: Any):
        self.d_stack.append(value)

    def interpret(self, chunk: Chunk) -> InterpretResult:
        self.chunk = chunk
        return self.run()

    def run(self) -> InterpretResult:
        while True:
            match (instruction := self.read_byte()):
                case Opcode.OP_CONSTANT:
                    constant = self.read_constant()
                    print_value(constant)
                    print()
                    break;
                case Opcode.OP_RETURN:
                    return InterpretResult.INTERPRET_OK
                case _:
                    return InterpretResult.INTERPRET_RUNTIME_ERROR

    def read_byte(self) -> int:
        instruction = self.chunk.code[self.ip]
        self.ip += 1
        return instruction

    def read_constant(self) -> Value:
        return self.chunk.constants[self.read_byte()]
