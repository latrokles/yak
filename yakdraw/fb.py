import ctypes

from dataclasses import dataclass, field

from yakdraw.color import Color, ColorFmt


@dataclass
class Framebuffer:
    w: int
    h: int
    fmt: ColorFmt
    mem: bytearray = field(init=False)

    def __post_init__(self):
        self.mem = bytearray(self.w * self.h * self.fmt.depth())

    @property
    def depth(self) -> int:
        return self.fmt.depth()

    def memory(self):
        return (ctypes.c_char * len(self.mem)).from_buffer(self.mem)

    def get_pixel(self, x: int, y: int) -> Color:
        """
        Return the value of the pixel at the x, y coordinates in framebuffer.

        :param x: x coordinate.
        :type x: int.

        :param y: y coordinate.
        :type y: int.

        :returns: the value of pixel at (`x`, `y`).
        :rtype: Color.

        :raises RuntimeError: if `x` and/or `y` values are out of bounds.
        """

        if (x < 0) or (x > self.w):
            raise RuntimeError(f'x={x} is out of framebuffer bounds')

        if (y <0) or (y > self.h):
            raise RuntimeError(f'y={y} is out of framebuffer bounds')
            
        pixel_0 = (y * (self.w * self.depth)) + (x * self.depth)
        pixel_n = (pixel_0 + self.depth)

        pixel_channels = self.mem[pixel_0:pixel_n]
        return Color.from_values(pixel_channels, self.fmt)

    def put_pixel(self, x: int, y: int, color: Color) -> None:
        """
        Set pixel value at the provided `x`, `y` coordinates in framebuffer to provided `color` value.

        :param x: x coordinate.
        :type x: int.

        :param y: y coordinate.
        :type y: int.

        :param color: the value to set the pixel to.
        :type colot: Color.

        :returns: None.
        """
        if (x < 0) or (x > self.w):
            return

        if (y < 0) or (y > self.h):
            return

        pixel_0 = (y * (self.w * self.depth)) + (x * self.depth)
        pixel_n = (pixel_0 + self.depth)
        self.mem[pixel_0:pixel_n] = color.to_values(self.fmt)

    def clear(self):
        self.mem = bytearray(self.w * self.h * self.depth)    