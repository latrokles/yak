from dataclasses import dataclass

from yak.color import Palette
from yak.draw import background, draw_line, draw_rect
from yak.sketch import Sketch


@dataclass
class Linescape(Sketch):
    margin: int = 20

    def setup(self):
        background(self.canvas, Palette.WHITE)

        draw_rect(self.canvas,
                  self.margin,
                  self.margin,
                  self.width - (self.margin * 2),
                  self.height - (self.margin * 2),
                  Palette.RED1)

        startx, starty = 20, 20
        endx, endy = self.width - 20, self.height - 20
        
        x0, y0 = startx, starty
        x1, y1 = startx, endy

        while (y0 < endy) and (x1 < endx):
            draw_line(self.canvas, x0, y0, x1, y1, Palette.random())
            y0 += 10
            x1 += 10

        while (x0 < endx) and (y1 > starty):
            draw_line(self.canvas, x0, y0, x1, y1, Palette.random())
            x0 += 10
            y1 -= 10