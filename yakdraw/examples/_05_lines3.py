import ctypes
import sdl2
import sys

from dataclasses import dataclass, field
from random import randint

from yakdraw.color import Palette
from yakdraw.draw import draw_line
from yakdraw.sketch import Sketch
from yakdraw.window import Mouse


WIDTH = 300
HEIGHT = 300
SCALE = 2


@dataclass
class Lines3(Sketch):
    points: list[tuple[int, int]] = field(default_factory=list)

    def setup(self):
        for y in range(self.height):
            for x in range(self.width):
                self.canvas.put_pixel(x, y, Palette.WHITE)

    def draw(self):
        if len(self.points) == 0:
            return

        p0 = self.points[0]
        for p1 in self.points[1:]:
            x0, y0 = p0
            x1, y1 = p1
            draw_line(self.canvas, x0, y0, x1, y1, Palette.RED)
            p0 = p1

    def handle_mouse(self, mouse: Mouse):
        if mouse.left:
            self.points.append((mouse.x, mouse.y))


def main():
    Lines3(WIDTH, HEIGHT, SCALE, title='lines2')