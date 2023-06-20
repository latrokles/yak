from dataclasses import dataclass
from random import randint

from yak.draw.color import Palette
from yak.draw.draw import background, draw_circle
from yak.draw.sketch import Sketch


@dataclass
class RandomCircles(Sketch):
    def setup(self):
        background(self.canvas, Palette.WHITE)

    def draw(self):
        x = randint(0, self.width)
        y = randint(0, self.height)
        r = randint(0, 100)

        draw_circle(self.canvas, x, y, r, Palette.random())
