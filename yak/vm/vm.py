from dataclasses import dataclass, field
from typing import Any


class VMError(Exception):
    """Raised whenever there is a VM execution error."""


@dataclass
class Closure:
    pass


@dataclass
class CallFrame:
    pass


@dataclass
class VirtualMachine:
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
