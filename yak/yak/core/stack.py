from dataclasses import dataclass, field

from yak.yak.core import YakError, YakPrimitive, YakVal

class UnderflowError(YakError):
    """Raised when stack doesn't have enough values."""


@dataclass
class Stack(YakPrimitive):
    """The core data structure in yak."""

    values: list[YakVal] = field(default_factory=list)

    @property
    def count(self) -> int:
        return len(self.values)

    def peek(self) -> YakVal:
        self.ensure(1)
        return self.values[-1]

    def pop(self) -> YakVal:
        self.ensure(1)
        return self.values.pop()

    def push(self, val: YakVal) -> None:
        self.values.append(val)

    def push_all(self, vals: list[YakVal]):
        self.values.extend(vals)

    def empty(self) -> bool:
        return self.count == 0

    def not_empty(self) -> bool:
        return not self.empty()

    def clear(self):
        self.values = []

    def fmt(self) -> str:
        pass

    def ensure(self, count: int):
        if count <= self.count:
            return

        raise UnderflowError(
            f'Not enough values in stack: expected={count}, actual={self.count}'
        )
