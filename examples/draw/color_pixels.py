from dataclasses import dataclass
from random import randint

from yak.draw.color import Palette
from yak.draw.draw import background, draw_point
from yak.draw.sketch import Sketch
from yak.draw.window import Mouse


@dataclass
class ColorPixels(Sketch):

      def mouse_updated(self):
          if self.mouse.left:
             draw_point(self.canvas, self.mouse.x, self.mouse.y, Palette.BLUE)
             return

      def setup(self):
          background(self.canvas, Palette.WHITE)

      def draw(self):
          x = randint(0, self.width)
          y = randint(0, self.height)

          draw_point(self.canvas, x, y, Palette.random())
