import os
import sys

EXAMPLES_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.dirname(EXAMPLES_DIR))

from draw.canvas_bounds import CanvasBounds
from draw.color_pixels import ColorPixels
from draw.linescape import Linescape
from draw.mouse_circles import MouseCircles
from draw.random_circles import RandomCircles
from draw.random_lines import RandomLines
from draw.simple_linepen import Linepen
from draw.triangles import Triangles


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


if __name__ == '__main__':
    main()
