from dataclasses import dataclass
from random import randint

from yak.color import Palette
from yak.draw import background, draw_triangle
from yak.sketch import Sketch


@dataclass
class Triangles(Sketch):
    def setup(self):
        background(self.canvas, Palette.WHITE)

    def draw(self):
        background(self.canvas, Palette.WHITE)
        x0 = randint(0, self.width)
        y0 = randint(0, self.height)
        x1 = randint(0, self.width)
        y1 = randint(0, self.height)
        x2 = randint(0, self.width)
        y2 = randint(0, self.height)

        draw_triangle(self.canvas, x0, y0, x1, y1, x2, y2, Palette.random())