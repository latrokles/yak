import ctypes
import sdl2
import sys

from dataclasses import dataclass
from random import randint

from yakdraw.color import Palette
from yakdraw.draw import draw_line
from yakdraw.sketch import Sketch
from yakdraw.window import Mouse


WIDTH = 300
HEIGHT = 300
SCALE = 2


@dataclass
class Lines2(Sketch):

    def setup(self):
        for y in range(self.height):
            for x in range(self.width):
                self.canvas.put_pixel(x, y, Palette.WHITE)

        startx, starty = 20, 20
        endx, endy = self.width - 20, self.height - 20
        
        x0, y0 = startx, starty
        x1, y1 = startx, endy

        while (y0 <= endy) and (x1 <= endx):
            draw_line(self.canvas, x0, y0, x1, y1, Palette.random())
            y0 += 10
            x1 += 10

        while (x0 <= endx) and (y1 >= starty):
            draw_line(self.canvas, x0, y0, x1, y1, Palette.random())
            x0 += 10
            y1 -= 10

def main():
    Lines2(WIDTH, HEIGHT, SCALE, title='lines2')