from dataclasses import dataclass
from random import randint

from yak.color import Palette
from yak.draw import draw_line
from yak.sketch import Sketch


@dataclass
class RandomLines(Sketch):

    def setup(self):
        for y in range(self.height):
            for x in range(self.width):
                self.canvas.put_pixel(x, y, Palette.WHITE)

    def draw(self) -> None:
        x = randint(20, self.width - 20)
        y = randint(20, self.height - 20)

        x1 = randint(20, self.width - 20)
        y1 = randint(20, self.height - 20)

        draw_line(self.canvas, x, y, x1, y1, Palette.random())