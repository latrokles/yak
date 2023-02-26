import ctypes
import sdl2
import sys


from yakdraw.window import Window


WIN_WIDTH = 640
WIN_HEIGHT = 480
SCALE = 2

def test():
    window = Window('sdltest', WIN_WIDTH, WIN_HEIGHT, SCALE)
    window.open()