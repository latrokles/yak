from dataclasses import dataclass
from random import randint

from yakdraw.color import Palette
from yakdraw.draw import draw_circle
from yakdraw.sketch import Sketch


@dataclass
class RandomCircles(Sketch):
    def setup(self):
        for y in range(self.height):
            for x in range(self.width):
                self.canvas.put_pixel(x, y, Palette.WHITE)

    def draw(self):
        x = randint(0, self.width)
        y = randint(0, self.height)
        r = randint(0, 100)

        draw_circle(self.canvas, x, y, r, Palette.random())