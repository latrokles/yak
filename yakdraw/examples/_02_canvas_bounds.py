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
    margin: int = 20

    def setup(self):
        for y in range(self.height):
            for x in range(self.width):
                self.canvas.put_pixel(x, y, Palette.WHITE)

    def draw(self) -> None:
        self.canvas.put_pixel(self.margin, self.margin, self.stroke)
        self.canvas.put_pixel(self.width - self.margin, self.margin, self.stroke)
        self.canvas.put_pixel(self.margin, self.height - self.margin, self.stroke)
        self.canvas.put_pixel(self.width - self.margin, self.height - self.margin, self.stroke)


def main():
    CanvasBounds(WIDTH, HEIGHT, SCALE, title='CanvasBounds')