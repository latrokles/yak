from dataclasses import dataclass, field


@dataclass
class Chunk:
    code: bytearray = field(default_factory=bytearray)

    @property
    def count(self) -> int:
        return len(self.code)

    def write(self, byte: int):
        self.code.append(byte)
