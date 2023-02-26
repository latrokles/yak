import ctypes
import sdl2
import sys

from dataclasses import dataclass

from yakdraw.color import Color, Palette
from yakdraw.sketch import Sketch
from yakdraw.window import Mouse


WIDTH = 320
HEIGHT = 240
SCALE = 2


@dataclass
class CanvasBounds(Sketch):
    stroke: Color = Palette.RED

    def setup(self):
        for y in range(self.height):
            for x in range(self.width):
                self.canvas.put_pixel(x, y, Palette.WHITE)

    def draw(self) -> None:
        self.canvas.put_pixel(5, 5, self.stroke)
        self.canvas.put_pixel(315, 5, self.stroke)
        self.canvas.put_pixel(5, 235, self.stroke)
        self.canvas.put_pixel(315, 235, self.stroke)


def main():
    CanvasBounds(WIDTH, HEIGHT, SCALE, title='CanvasBounds')