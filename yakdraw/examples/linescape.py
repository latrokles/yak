from dataclasses import dataclass

from yakdraw.color import Palette
from yakdraw.draw import draw_line
from yakdraw.sketch import Sketch


@dataclass
class Linescape(Sketch):
    margin: int = 20

    def setup(self):
        for y in range(self.height):
            for x in range(self.width):
                self.canvas.put_pixel(x, y, Palette.WHITE)

        # this could be a rect!
        draw_line(self.canvas,
                  self.margin,
                  self.margin,
                  self.width - self.margin,
                  self.margin,
                  Palette.RED1)

        draw_line(self.canvas,
                  self.width - self.margin,
                  self.margin,
                  self.width - self.margin,
                  self.height - self.margin,
                  Palette.RED1)

        draw_line(self.canvas,
                  self.width - self.margin,
                  self.height - self.margin,
                  self.margin,
                  self.height - self.margin,
                  Palette.RED1)

        draw_line(self.canvas,
                  self.margin,
                  self.height - self.margin,
                  self.margin,
                  self.margin,
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