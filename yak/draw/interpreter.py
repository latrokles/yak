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
                return 'ok!'
            case 'fill-random':
                self.hal.screen.fill(Palette.random())
                return 'ok!'
            case 'draw-line':
                self.draw_diagonal()
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

    def draw_diagonal(self):
        brush = Form(0, 0, 2, 2, ColorFmt.RGBA)
        brush.fill(Palette.SKYBLUE1)
        BitBlt(
            destination=self.hal.screen,
            source=brush,
            fill=None,
            combination_rule=CombinationRule.SOURCE_ONLY,
            destination_x=0,
            destination_y=0,
            source_x=0,
            source_y=0,
            width=brush.w,
            height=brush.h,
            clip_x=0,
            clip_y=0,
            clip_w=self.hal.screen.w,
            clip_h=self.hal.screen.h
        ).draw_line(0, 0, self.hal.screen.w - 10, self.hal.screen.h - 10)
