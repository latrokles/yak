from dataclasses import dataclass, field

from yak.color import Color, Palette
from yak.sketch import Sketch


@dataclass
class CanvasBounds(Sketch):
    stroke: Color = field(init=False)
    margin: int = 20

    def setup(self):
        self.stroke = Palette.RED1
        for y in range(self.height):
            for x in range(self.width):
                self.canvas.put_pixel(x, y, Palette.WHITE)

    def draw(self) -> None:
        self.canvas.put_pixel(self.margin, self.margin, self.stroke)
        self.canvas.put_pixel(self.width - self.margin, self.margin, self.stroke)
        self.canvas.put_pixel(self.margin, self.height - self.margin, self.stroke)
        self.canvas.put_pixel(self.width - self.margin, self.height - self.margin, self.stroke)