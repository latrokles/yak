from enum import IntEnum, auto

class Opcode(IntEnum):
    OP_CONSTANT      = 0x00
    OP_DEFINE_GLOBAL = auto()
    OP_GET_GLOBAL    = auto()
    OP_ADD           = auto()
    OP_SUBTRACT      = auto()
    OP_MULTIPLY      = auto()
    OP_DIVIDE        = auto()
    OP_NEGATE        = auto()
    OP_PRINT         = auto()
    OP_RETURN        = auto()
