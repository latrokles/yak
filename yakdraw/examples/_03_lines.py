import ctypes
import sdl2
import sys

from dataclasses import dataclass
from random import randint

from yakdraw.color import Palette
from yakdraw.draw import draw_line
from yakdraw.sketch import Sketch
from yakdraw.window import Mouse


WIDTH = 320
HEIGHT = 240
SCALE = 2


@dataclass
class Lines(Sketch):

    def setup(self):
        for y in range(self.height):
            for x in range(self.width):
                self.canvas.put_pixel(x, y, Palette.WHITE)

    def draw(self) -> None:
        x = randint(0, self.width)
        y = randint(0, self.height)

        x1 = randint(0, self.width)
        y1 = randint(0, self.height)

        draw_line(self.canvas, x, y, x1, y1, Palette.random())

def main():
    Lines(WIDTH, HEIGHT, SCALE, title='lines')
         