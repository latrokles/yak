from dataclasses import dataclass
from random import randint

from yakdraw.color import Palette
from yakdraw.sketch import Sketch
from yakdraw.window import Mouse


@dataclass
class ColorPixels(Sketch):

      def mouse_updated(self):
          if self.mouse.left:
             self.canvas.put_pixel(self.mouse.x, self.mouse.y, Palette.BLUE)
             return

      def setup(self):
          for y in range(self.height):
              for x in range(self.width):
                  self.canvas.put_pixel(x, y, Palette.WHITE)

      def draw(self):
          x = randint(0, self.width)
          y = randint(0, self.height)

          self.canvas.put_pixel(x, y, Palette.random())