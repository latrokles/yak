from yak.vm.debug import disassemble_chunk
from yak.vm.chunk import Chunk
from yak.vm.opcode import Opcode
from yak.vm.vm import VirtualMachine


def yak():
    vm = VirtualMachine()

    chunk = Chunk()
    value = chunk.add_constant(1.2)
    chunk.write(Opcode.OP_CONSTANT, 123)
    chunk.write(value, 123)

    value = chunk.add_constant(3.4)
    chunk.write(Opcode.OP_CONSTANT, 123)
    chunk.write(value, 123)

    chunk.write(Opcode.OP_ADD, 123)

    value = chunk.add_constant(5.6)
    chunk.write(Opcode.OP_CONSTANT, 123)
    chunk.write(value, 123)

    chunk.write(Opcode.OP_DIVIDE, 123)

    chunk.write(Opcode.OP_NEGATE, 123)
    chunk.write(Opcode.OP_RETURN, 123)

    vm.interpret(chunk)
