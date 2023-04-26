from yak.vm.chunk import Chunk
from yak.vm.opcode import Opcode


def yak():
    chunk = Chunk()
    chunk.write(Opcode.OP_RETURN)
    pass
