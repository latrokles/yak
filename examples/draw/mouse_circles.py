from dataclasses import dataclass
from random import randint

from yak.draw.color import Palette
from yak.draw.draw import background, draw_circle
from yak.draw.sketch import Sketch


@dataclass
class MouseCircles(Sketch):
    def setup(self):
        background(self.canvas, Palette.WHITE)

    def draw(self):
        if self.mouse.left:
            draw_circle(self.canvas, self.mouse.x, self.mouse.y, randint(30, 100), Palette.random())
