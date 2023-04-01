from dataclasses import dataclass
from random import randint

from yak.color import Palette
from yak.draw import background, draw_line
from yak.sketch import Sketch


@dataclass
class RandomLines(Sketch):

    def setup(self):
        background(self.canvas, Palette.WHITE)

    def draw(self) -> None:
        x = randint(20, self.width - 20)
        y = randint(20, self.height - 20)

        x1 = randint(20, self.width - 20)
        y1 = randint(20, self.height - 20)

        draw_line(self.canvas, x, y, x1, y1, Palette.random())
