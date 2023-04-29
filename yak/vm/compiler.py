from dataclasses import dataclass

from yak.vm.chunk import Chunk
from yak.vm.debug import DEBUG_PRINT_CODE, disassemble_chunk
from yak.vm.opcode import Opcode
from yak.vm.parser import Parser
from yak.vm.scanner import Scanner
from yak.vm.value import Value


@dataclass
class Compiler:
    compiling_chunk: Chunk|None = None 

    def compile(self, source: str, chunk: Chunk) -> bool:
        try:
            self.compiling_chunk = chunk
            scanner = Scanner(source)
            parser = Parser(self, scanner).parse()
            self.emit_return(scanner.row)
            if DEBUG_PRINT_CODE:
                disassemble_chunk(self.current_chunk, 'code')
            return True
        except:
            return False

    @property
    def current_chunk(self) -> Chunk:
        return self.compiling_chunk

    def make_constant(self, value: Value) -> int:
        return self.current_chunk.add_constant(value)

    def emit_byte(self, byte: int, line: int) -> None:
        self.current_chunk.write(byte, line) 

    def emit_bytes(self, byte1: int, byte2: int, line: int) -> None:
        self.emit_byte(byte1, line)
        self.emit_byte(byte2, line)

    def emit_return(self, line: int):
        self.emit_byte(Opcode.OP_RETURN, line)
