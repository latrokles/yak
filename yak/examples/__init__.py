import sys

from yak.examples.canvas_bounds import CanvasBounds
from yak.examples.color_pixels import ColorPixels
from yak.examples.linescape import Linescape
from yak.examples.mouse_circles import MouseCircles
from yak.examples.random_circles import RandomCircles
from yak.examples.random_lines import RandomLines
from yak.examples.simple_linepen import Linepen
from yak.examples.triangles import Triangles



options = {
    'colorpixels': ('paint pixels and use mouse input',
                    lambda: ColorPixels(600, 400, 1, title='ColorPixels')),
    'canvasbounds': ('test canvas coordinate system',
                     lambda: CanvasBounds(320, 280, 2, title='CanvasBounds')),
    'mousecircle': ('mouse and circle drawing',
                    lambda: MouseCircles(300, 300, 2, title='circles')),
    'randomlines': ('line drawing and palette selection',
                    lambda: RandomLines(300, 300, 2, title='random lines')),
    'randomcircles': ('circle drawing',
                      lambda: RandomCircles(300, 300, 2, title='random circles')),
    'linescape': ('more line drawing',
                  lambda: Linescape(300, 300, 2, title='linescape')),
    'linepen': ('simple line "pen"',
                lambda: Linepen(300, 300, 2, title='simple linepen')),
    'triangles': ('simple triangles',
                  lambda: Triangles(300, 300, 1, title='triangles')),
    'quit': ('quit examples', quit) 
}


def quit():
    print('bye!')
    sys.exit(0)


def display_options():
    print('Examples:')
    print('---------')
    for option, value in options.items():
        print(f'- {option}:  {value[0]}')
    print()


def main():
    while True:
        display_options()
        selection = input('enter the example to run: ')

        _, program = options.get(selection, (None, None))
        if program is None:
            print()
            print(f'`{selection}` is not a valid example!\n')
            continue
        program()
        
    