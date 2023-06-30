from .color import ColorFmt, Palette
from .form import Form, OutOfBoundsError
from .bitblt import CombinationRule, BitBlt, BitBltError


def simple_draw(hal):
    return SimpleDrawer(hal)


class SimpleDrawer:
    def __init__(self, hal):
        self.hal = hal

    def interpret(self, expression):
        match expression:
            case 'draw-square':
                self.draw_square()
            case 'fill-random':
                self.hal.screen.fill(Palette.random())
                return 'ok!'
            case 'exit':
                self.hal.exit_signalled = True
                return 'bye!'
            case _:
                return f'cannot evaluate expression: `{expression}`'

    def draw_square(self):
        square = Form(0, 0, 100, 100, ColorFmt.RGBA)
        square.fill(Palette.YELLOW3)
        BitBlt(
            destination=self.hal.screen,
            source=square,
            fill=None,
            combination_rule=CombinationRule.SOURCE_ONLY,
            destination_x=int(self.hal.screen.w / 2 - 50),
            destination_y=int(self.hal.screen.h / 2 - 50),
            source_x=0,
            source_y=0,
            width=square.w,
            height=square.h,
            clip_x=0,
            clip_y=0,
            clip_w=self.hal.screen.w,
            clip_h=self.hal.screen.h
        ).copy_bits()
