from dataclasses import dataclass
from random import randint

from yakdraw.color import Palette
from yakdraw.draw import draw_circle
from yakdraw.sketch import Sketch


@dataclass
class MouseCircles(Sketch):
    def setup(self):
        for y in range(self.height):
            for x in range(self.width):
                self.canvas.put_pixel(x, y, Palette.WHITE)

    def draw(self):
        if self.mouse.left:
            draw_circle(self.canvas, self.mouse.x, self.mouse.y, randint(30, 100), Palette.random())