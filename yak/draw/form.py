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

    def row_bytes(self, x, y, pixel_count):
        print(f'reading `{pixel_count}` pixels in row `{y}` starting in col `{x}`')
        if x + (pixel_count - 1) >= self.w:
            raise OutOfBoundsError(f'reading beyond bitmap width. start={x}, pixels={pixel_count}, bitmap width={self.w}')

        byte_0 = (y * (self.w * self.depth)) + (x * self.depth)
        byte_n = byte_0 + (self.depth * (pixel_count - 1))
        return self.bitmap[byte_0:byte_n]

    def put_row_bytes(self, x, y, row_bytes):
        if x + ((len(row_bytes) - 1) / self.depth) >= self.w:
            raise OutOfBoundsError(f'writing beyond bitmap width. start={x}, pixel_count={len(row_bytes) / self.depth}')

        byte_0 = (y * (self.w * self.depth)) + (x * self.depth)
        byte_n = byte_0 + len(row_bytes)
        self.bitmap[byte_0:byte_n] = row_bytes

    def fill(self, color):
        self.bitmap = bytearray(self.w * self.h * color.to_values(self.color_format))

    def draw_on(self, medium, x, y, clip_x, clip_y, clip_w, clip_h, rule, fill):
        # implement using bitblt
        # bitblt = BitBlt(
        #     destination=medium,
        #     source=self,
        #     fill=fill,
        #     combination_rule=rule,
        #     destination_x=x,
        #     destination_y=y,
        #     source_x=self.x,
        #     source_y=self.y,
        #     extent=(self.w, self.y),
        #     clip_x=clip_x,
        #     clip_y=clip_y,
        #     clip_w=clip_w,
        #     clip_h=clip_h
        # )
        # bitblt.copy_bits()
        pass

    def _pixel_bytes_range_at_point(self, x, y) -> tuple[int,int]:
        x_out_of_bounds = x < 0 or self.w <= x
        y_out_of_bounds = y < 0 or self.h <= y
        if x_out_of_bounds or y_out_of_bounds:
            raise OutOfBoundsError(f'{point} is out of bounds of {self}')

        byte_0 = (y * (self.w * self.depth)) + (x * self.depth)
        byte_n = byte_0 + self.depth
        return byte_0, byte_n
