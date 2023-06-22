from dataclasses import dataclass
from enum import IntEnum, auto

from .color import Color
from .geometry import Rectangle

"""
Exploring some of smalltalk's graphics primitives here
"""

@dataclass
class Bitmap:
    memory_bytes: bytearray


@dataclass
class Form:
    width: int
    height: int
    depth: int
    bitmap: Bitmap


class CombinationRule(Enum):
    ALL_ZEROS                            = 0
    SOURCE_AND_DESTINATION               = 1
    SOURCE_AND_DESTINATION_INVERT        = 2
    SOURCE_ONLY                          = 3
    SOURCE_INVERT_AND_DESTINATION        = 4
    DESTINATION_ONLY                     = 5
    SOURCE_XOR_DESTINATION               = 6
    SOURCE_OR_DESTINATION                = 7
    SOURCE_INVERT_AND_DESTINATION_INVERT = 8
    SOURCE_INVERT_XOR_DESTINATION        = 9
    DESTINATION_INVERT                   = 10
    SOURCE_OR_DESTINATION_INVERT         = 11
    SOURCE_INVERT                        = 12
    SOURCE_INVERT_OR_DESTINATION         = 13
    SOURCE_INVERT OR DESTINATION_INVERT  = 14
    ALL_ONES                             = 15


@dataclass
class BitBlt:
    destination:
    source:
    fill: Color
    combination_rule: CombinationRule
    destination_origin:
    source_origin:
    extent: Rectangle
    clipping_rect: Rectangle

    def draw_from_to(self):
        pass

    def draw_loop(self):
        pass

    def copy_bits(self):
        pass
