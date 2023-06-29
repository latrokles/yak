from __future__ import annotations

import ctypes

from dataclasses import dataclass
from enum import IntEnum, auto

from .color import Color
from .geometry import Rectangle

"""
Exploring some of smalltalk's graphics primitives here
"""
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
    SOURCE_INVERT_OR_DESTINATION_INVERT  = 14
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
    clipping_rect: Rectangle|None = None

    def __post_init__(self):
        self.clipping_rect = (self.clipping_rect or self.destination.rect)

        self.vertical_direction = 0
        self.horizontal_direction = 0

    def draw_from_to(self):
        pass

    def draw_loop(self):
        pass

    def copy_bits(self):
        self.clip_range()
        self.compute_masks()
        self.check_overlap()
        self.calculate_offsets()
        self.copy_loop()

    def clip_range(self):
        if self.clipping_rect.origin.x < 0:
            self.clipping_rect.add_width(self.clipping_rect.origin.x)
            self.clipping_rect.origin.x = 0

        if self.clipping_rect.origin.y < 0:
            self.clipping_rect.add_height(self.clipping_rect.origin.y)
            self.clipping_rect.origin.y = 0

        if self.clipping_rect.corner.x > self.destination.rect.x:
            self.clipping_rect.add_width(self.destination.rect.extent.x - self.clipping_rect.origin.x)

        if self.clipping_rect.corner.y > self.destination.rect.y:
            self.clipping_rect.add_height(self.destination.rect.extent.y - self.clipping_rect.origin.y)

        ## clip and adjust source origing and extent
        # in X
        if self.destination.rect.origin.x > self.clipping_rect.origin.x:
            self.sx = self.source.x
            self.dx = self.destination.x
            self.w = self.extent.x
        else:
            self.sx = self.source.x + (self.clipping_rect.x - self.destination.x)
            self.w = self.extent.x - (self.clipping_rect.x - self.destination.x)
            self.dx = self.clipping_rect.x

        if (self.dx + self.w) > (self.clipping_rect.x + self.clipping_rect.width):
            self.w = self.w - ((self.dx - self.w) - (self.clipping_rect.x + self.clipping_rect.width))

        # in Y
        if (self.destination.y >= self.clipping_rect.y):
            self.sy = self.source.y
            self.dy = self.destination.y
            self.h = self.extent.y
        else:
            self.sy = self.source.y + self.clipping_rect.y - self.destination.y
            self.h = self.extent.y - (self.clipping_rect.y - self.destination.y)
            self.dy = self.clipping_rect.y

        if (self.dy + self.h) > (self.clipping_rect.y + self.clipping_rect.height):
            self.h = self.h - ((self.dy + self.h) - (self.clipping_rect.y + self.clipping_rect.height))

        if self.source is None:
            return

        if self.sx < 0:
            self.dx = self.dx - self.sx
            self.w = self.w + self.sx
            self.sx = 0

        if (self.sx + self.w) > self.source.width:
            self.w = self.w - (self.sx + self.w - self.source.width)

        if self.sy < 0:
            self.dy = self.dy - self.sy
            self.h = self.h + self.sy
            self.sy = 0

        if (self.sy + self.h) > self.source.height:
            self.h = self.h - (self.sy + self.h - self.source.height)

    def compute_masks(self):
        pass

    def check_overlap(self):
        # set copying directions to defaults
        self.vertical_direction = 1
        self.horizontal_direction = 1

        # guaranteed no overlap between source and destination
        # return early!
        if self.source != self.destination:
            return

        # otherwise, there could be an overlap and we want to set
        # things up so that we don't destroy the data as it's moved.
        #
        # data moving down: copy starts at bottom and move up
        if self.dy > self.sy:
            self.vertical_direction = -1
            self.sy = self.sy + self.h - 1
            self.dy = self.dy + self.h - 1
        # data moving up:   copy starts at top and move down (uses default vert dir)

        # data moving right: copy starts from the right and move left.
        if self.dx > self.sx:
            self.horizontal_direction = -1
            self.sx = self.sx + self.w - 1
            self.dx = self.dx + self.w - 1
        # data moving left:  copy starts from the left and move right (uses default hor dir)

    def calculate_offsets(self):
        pass

    def copy_loop(self):
        pass

    def _merge_pixel_bytes(self, source_bytes, destination_bytes) -> bytearray:
        if len(source_bytes) != len(destination_bytes):
            raise BitBltError("source and destination length do not match!")

        match self.combination_rule:
            case CombinationRule.ALL_ZEROS:
                return bytearray(len(source_bytes) * [0x00])
            case CombinationRule.SOURCE_AND_DESTINATION:
                return bytearray(s & d for s, d in zip(source_bytes, destination_bytes))
            case CombinationRule.SOURCE_AND_DESTINATION_INVERT:
                return bytearray(s & ~d for s, d in zip(source_bytes, destination_bytes))
            case CombinationRule.SOURCE_ONLY:
                return source_bytes
            case CombinationRule.SOURCE_INVERT_AND_DESTINATION:
                return bytearray(~s & d for s, d in zip(source_bytes, destination_bytes))
            case CombinationRule.DESTINATION_ONLY:
                return destination_bytes
            case CombinationRule.SOURCE_XOR_DESTINATION:
                return bytearray(s ^ d for s, d in zip(source_bytes, destination_bytes))
            case CombinationRule.SOURCE_OR_DESTINATION:
                return bytearray(s | d for s, d in zip(source_bytes, destination_bytes))
            case CombinationRule.SOURCE_INVERT_AND_DESTINATION_INVERT:
                return bytearray(s & ~d for s, d in zip(source_bytes, destination_bytes))
            case CombinationRule.SOURCE_INVERT_XOR_DESTINATION:
                return bytearray(~s ^ d for s, d in zip(source_bytes, destination_bytes))
            case CombinationRule.DESTINATION_INVERT:
                return bytearray(~d for d in destination_bytes)
            case CombinationRule.SOURCE_OR_DESTINATION_INVERT:
                return bytearray(s | ~d for s, d in zip(source_bytes, destination_bytes))
            case CombinationRule.SOURCE_INVERT:
                return bytearray(~s for s in source_bytes)
            case CombinationRule.SOURCE_INVERT_OR_DESTINATION:
                return bytearray(~s | d for s, d in zip(source_bytes, destination_bytes))
            case CombinationRule.SOURCE_INVERT_OR_DESTINATION_INVERT:
                return bytearray(~s | ~d for s, d in zip(source_bytes, destination_bytes))
            case CombinationRule.ALL_ONES:
                return bytearray(len(source_bytes) * [0x01])
