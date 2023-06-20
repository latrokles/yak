from dataclasses import dataclass, field

from yak.draw.color import Color, Palette
from yak.draw.draw import background, draw_point
from yak.draw.sketch import Sketch


@dataclass
class CanvasBounds(Sketch):
    stroke: Color = field(init=False)
    margin: int = 20

    def setup(self):
        self.stroke = Palette.RED1
        background(self.canvas, Palette.WHITE)

    def draw(self) -> None:
        draw_point(self.canvas, self.margin, self.margin, self.stroke)
        draw_point(self.canvas, self.width - self.margin, self.margin, self.stroke)
        draw_point(self.canvas, self.margin, self.height - self.margin, self.stroke)
        draw_point(self.canvas, self.width - self.margin, self.height - self.margin, self.stroke)
