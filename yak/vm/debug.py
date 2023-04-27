from yak.util import getenv_bool
from yak.vm.chunk import Chunk
from yak.vm.opcode import Opcode
from yak.vm.value import print_value

DEBUG_TRACE_EXECUTION = getenv_bool('TRACE_EXECUTION', False)


def disassemble_chunk(chunk: Chunk, name: str) -> None:
    print(f'== {name} ==')
    offset = 0
    while offset < chunk.count:
        offset = disassemble_instruction(chunk, offset)


def disassemble_instruction(chunk: Chunk, offset: int) -> int:
    print(f'{offset:04d} ', end='')

    if offset > 0 and chunk.lines[offset] == chunk.lines[offset-1]:
        print('   | ', end='')
    else:
        print(f'{chunk.lines[offset]:04d} ', end='')


    instruction = chunk.code[offset]
    match instruction:
        case Opcode.OP_CONSTANT:
            return constant_instruction('OP_CONSTANT', chunk, offset)
        case Opcode.OP_RETURN:
            return simple_instruction('OP_RETURN', offset)
        case _:
            print(f'Unknown opcode {instruction:d}')
            return offset + 1


def constant_instruction(name: str, chunk: Chunk, offset: int) -> int:
    const = chunk.code[offset]
    print(f'{name:16s} {const} "', end='')
    print_value(chunk.constants[const])
    print('"')
    return offset + 2


def simple_instruction(name: str, offset: int) -> int:
    print(f'{name}')
    return offset + 1