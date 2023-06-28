import ctypes

from dataclasses import dataclass

from .color import Color, ColorFmt


class OutOfBoundsError(Exception):
    """Raised when trying to access a location outside a form."""


@dataclass
class Form:
    x: int
    y: int
    w: int
    h: int
    color_format: ColorFmt
    bitmap: bytearray|None = None

    def __post_init__(self):
        if self.bitmap is None:
            self.bitmap = bytearray(self.w * self.h * self.depth * [0x00])

    @property
    def depth(self):
        return self.color_format.depth()

    @property
    def bitmap_bytes(self):
        return (ctypes.c_char * len(self.bitmap)).from_buffer(self.bitmap)

    def color_at(self, x, y):
        _0th, _nth = self._pixel_bytes_range_at_point(x, y)
        pixel_bytes = self.bitmap[_0th:_nth]
        return Color.from_values(pixel_bytes, self.color_format)

    def put_color_at(self, x, y, color) -> None:
        _0th, _nth = self._pixel_bytes_range_at_point(x, y)
        self.bitmap[_0th:_nth] = color.to_values(self.color_format)

    def fill(self, color):
        self.bitmap = bytearray(self.w * self.h * color.to_values(self.color_format))

    def _pixel_bytes_range_at_point(self, x, y) -> tuple[int,int]:
        x_out_of_bounds = x < 0 or self.w <= x
        y_out_of_bounds = y < 0 or self.h <= y
        if x_out_of_bounds or y_out_of_bounds:
            raise OutOfBoundsError(f'{point} is out of bounds of {self}')

        byte_0 = (y * (self.w * self.depth)) + (x * self.depth)
        byte_n = byte_0 + self.depth
        return byte_0, byte_n
