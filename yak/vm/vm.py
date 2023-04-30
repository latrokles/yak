from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Callable

from yak.vm.chunk import Chunk
from yak.vm.compiler import Compiler
from yak.vm.debug import DEBUG_TRACE_EXECUTION, disassemble_instruction
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

    d_stack: list[Value] = field(default_factory=list)       # TODO limit data stack size?
    c_stack: list[CallFrame] = field(default_factory=list)
    GLOBALS: dict[str, Value] = field(default_factory=dict)

    def reset_stack(self) -> None:
        self.d_stack = []

    def peek_value(self) -> Value:
        return self.d_stack[-1]

    def pop_value(self) -> Value:
        return self.d_stack.pop()

    def push_value(self, value: Value):
        self.d_stack.append(value)

    def interpret(self, source: str) -> InterpretResult:
        chunk = Chunk()
        if not Compiler().compile(source, chunk):
            return InterpretResult.INTERPRET_COMPILE_ERROR

        self.chunk = chunk
        self.ip = 0
        return self.run()

    def run(self) -> InterpretResult:
        while True:
            if DEBUG_TRACE_EXECUTION:
                print('          ', end='')
                for val in self.d_stack:
                    print('[ ', end='')
                    print_value(val)
                    print(' ]', end='')
                print()
                disassemble_instruction(self.chunk, self.ip)

            instruction = self.read_byte()
            match instruction:
                case Opcode.OP_CONSTANT:
                    constant = self.read_constant()
                    self.push_value(constant)
                case Opcode.OP_DEFINE_GLOBAL:
                    value = self.pop_value()
                    const = self.pop_value()
                    self.GLOBALS[const] = value
                case Opcode.OP_GET_GLOBAL:
                    const = self.pop_value()
                    self.push_value(self.GLOBALS[const])
                case Opcode.OP_ADD:
                    self.binary_op(lambda a, b: a + b)
                case Opcode.OP_SUBTRACT:
                    self.binary_op(lambda a, b: a - b)
                case Opcode.OP_MULTIPLY:
                    self.binary_op(lambda a, b: a * b)
                case Opcode.OP_DIVIDE:
                    self.binary_op(lambda a, b: a / b)
                case Opcode.OP_NEGATE:
                    # TODO replace in place ?
                    self.push_value(-self.pop_value())
                case Opcode.OP_PRINT:
                    print_value(self.pop_value())
                    print()
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

    def binary_op(self, func: Callable) -> None:
        b = self.pop_value()
        a = self.pop_value()
        self.push_value(func(a, b))
