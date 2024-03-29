from dataclasses import dataclass, field

from yak.draw.color import Palette
from yak.draw.draw import background, draw_line
from yak.draw.sketch import Sketch
from yak.draw.window import Mouse


@dataclass
class Linepen(Sketch):
    points: list[tuple[int, int]] = field(default_factory=list)

    def setup(self):
        background(self.canvas, Palette.WHITE)

    def draw(self):
        if len(self.points) == 0:
            return

        p0 = self.points[0]
        for p1 in self.points[1:]:
            x0, y0 = p0
            x1, y1 = p1
            draw_line(self.canvas, x0, y0, x1, y1, Palette.RED)
            p0 = p1

    def mouse_updated(self):
        if self.mouse.left:
            self.points.append((self.mouse.x, self.mouse.y))
