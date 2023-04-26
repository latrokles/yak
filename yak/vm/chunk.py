from dataclasses import dataclass, field

from yak.vm.value import Value


@dataclass
class Chunk:
    code: bytearray = field(default_factory=bytearray)
    constants: list[Value] = field(default_factory=list)
    lines: list[int] = field(default_factory=list)

    @property
    def count(self) -> int:
        return len(self.code)

    @property
    def constants_count(self) -> int:
        return len(self.constants)

    def write(self, byte: int, line: int):
        self.code.append(byte)
        self.lines.append(line)

    def add_constant(self, const: Value) -> int:
        self.constants.append(const)
        return self.constants_count - 1
