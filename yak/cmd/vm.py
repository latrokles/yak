from yak.vm.debug import disassemble_chunk
from yak.vm.chunk import Chunk
from yak.vm.opcode import Opcode


def yak():
    chunk = Chunk()
    value = chunk.add_constant(1.2)
    chunk.write(Opcode.OP_CONSTANT, 123)
    chunk.write(value, 123)
    chunk.write(Opcode.OP_RETURN, 123)
    disassemble_chunk(chunk, 'test chunk')
