from __future__ import annotations

import ctypes

from dataclasses import dataclass
from enum import IntEnum, auto

from .color import Color
from .geometry import Rectangle

"""
Exploring some of smalltalk's graphics primitives here
"""

class OutOfBoundsError(Exception):
    """Raised when trying to access a location outside a form."""


@dataclass
class Form:
    width: int
    height: int
    color_format: ColorFmt
    bitmap: bytearray
    rect: Rectangle = field(init=False)

    def __post_init__(self):
        self.rect = Rectangle.from_coordinates_and_dimensions(0, 0, self.width, self.height)

    @property
    def depth(self) -> int:
        return self.color_format.depth()

    @property
    def bitmap_bytes(self):
        return (ctypes.c_char * len(self.bitmap)).from_buffer(self.bitmap)

    def color_at(self, point: Point) -> Color:
        _0th, _nth = self._pixel_bytes_range_at_point(point)
        pixel_bytes = self.bitmap[_0th:_nth]
        return Color.from_values(pixel_bytes, self.fmt)

    def put_color_at(self, point: Point, color: Color) -> None:
        _0th, _nth = self._pixel_bytes_range_at_point(point)
        self.bitmap[_0th:_nth] = color.to_values(self.fmt)

    def display_on(self,
                   medium: Form,
                   at: Point,
                   clipping_rect: Rectangle|None = None,
                   rule: CombinationRule|None = None,
                   fill: Color|None = None) -> None:
        # TODO set defaults

        bitblt = BitBlt(
            destination=medium,
            source=self,
            fill=fill,
            combination_rule=rule,
            destination_origin=at,
            source_origin=self.rect.origin,
            extent=self.rect.corner,
            clipping_rect=clipping_rect
        )
        bitblt.copy_bits()

    def fill(self, color: Color) -> None:
        self.bitmap = bytearray(self.width * self.height * self.width * color.to_values)

    def _pixel_bytes_range_at_point(self, point: Point) -> tuple[int,int]:
        if not self.rect.contains_point(point):
            raise OutOfBoundsError(f'{point} is out of bounds of {self}')

        byte_0 = (point.y * (self.width * self.depth)) + (point.x * self.depth)
        byte_n = byte_0 + self.depth
        return byte_0, byte_n




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
    destination: Form
    source: Form
    fill: Color
    combination_rule: CombinationRule
    destination_origin: Point
    source_origin: Point
    extent: Rectangle
    clipping_rect: Rectangle

    def draw_from_to(self):
        pass

    def draw_loop(self):
        pass

    def copy_bits(self):
        pass
