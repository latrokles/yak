import ctypes
import sdl2
import sys

from dataclasses import dataclass

from yak.color import Palette
from yak.sketch import Sketch
from yak.window import Mouse


WIDTH = 320
HEIGHT = 240
SCALE = 2


@dataclass
class SdlTestSketch(Sketch):
    def setup(self):
        for y in range(self.height):
            for x in range(self.width):
                self.canvas.put_pixel(x, y, Palette.WHITE)

    def handle_mouse(self, mouse: Mouse):
        if mouse.left:
            self.canvas.put_pixel(mouse.x, mouse.y, Palette.BLUE)
            return

def test():
    SdlTestSketch(WIDTH, HEIGHT, SCALE, title='sdltestsketch')
