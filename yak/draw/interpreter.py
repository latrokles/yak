from .color import Color, ColorFmt, Palette
from .form import Form, OutOfBoundsError
from .bitblt import CombinationRule, BitBlt, BitBltError


def is_int(val: str) -> bool:
    try:
        int(val)
        return True
    except ValueError:
        return False


def is_float(val: str) -> bool:
    try:
        float(val)
        return True
    except ValueError:
        return False


def simple_draw(hal):
    return SimpleDrawer(hal)


class SimpleDrawer:
    def __init__(self, hal):
        self.hal = hal
        self.vocab = {
            'set': self.set_global,
            'get': self.get_global,
            'exit': self.exit,
            'rgb': self.rgb,
            'square': self.square,
            'rgb': self.rgb,
            'brush': self.brush,
            'draw': self.draw,
            'draw-line': self.draw_line,
        }
        self._globals = {
            'screen': self.hal.screen
        }
        self.stack = []

    def interpret(self, expression):
        try:
            return self.eval(self.read(expression))
        except Exception as e:
            return f'there was an error={e}'

    def read(self, source):
        return source.split(' ')

    def eval(self, tokens):
        for token in tokens:
            ret = self.eval_token(token)
        return ret

    def eval_token(self, token):
        if token ==  '':
            return ''

        if token in self.vocab.keys():
            self.execute(token)
            return 'ok!'

        if is_int(token):
            self.stack.append(int(token))
            return 'ok!'

        if is_float(token):
            self.stack.append(float(token))
            return 'ok!'

        if token[0] == "'" and token[-1] == "'":
            self.stack.append(token[1:-1])
            return 'ok!'

        raise RuntimeError(f'invalid token: `{token}`')

    def prnt(self):
        val = self.stack.pop()
        print(val)
        return val

    def execute(self, fn):
        defn = self.vocab[fn]
        defn()

    def exit(self):
        self.hal.exit_signalled = True

    def set_global(self):
        var = self.stack.pop()
        val = self.stack.pop()
        self._globals[var] = val

    def get_global(self):
        var = self.stack.pop()
        self.stack.append(self._globals[var])

    def rgb(self):
        b = self.stack.pop()
        g = self.stack.pop()
        r = self.stack.pop()
        self.stack.append(Color(r, g, b))

    def square(self):
        color = self.stack.pop()
        width = self.stack.pop()
        height = self.stack.pop()
        square = Form(0, 0, width, height, ColorFmt.RGBA)
        square.fill(color)
        self.stack.append(square)

    def brush(self):
        self.square()

    def draw(self):
        dst = self.stack.pop()
        src = self.stack.pop()
        x = self.stack.pop()
        y = self.stack.pop()

        BitBlt(
            dst,
            src,
            fill=None,
            combination_rule=CombinationRule.SOURCE_ONLY,
            destination_x=x,
            destination_y=y,
            source_x=src.x,
            source_y=src.y,
            width=src.w,
            height=src.h,
            clip_x=0,
            clip_y=0,
            clip_w=dst.w,
            clip_h=dst.h
        ).copy_bits()

    def draw_line(self):
        y1 = self.stack.pop()
        x1 = self.stack.pop()
        y0 = self.stack.pop()
        x0 = self.stack.pop()
        dst = self.stack.pop()
        brush = self.stack.pop()

        BitBlt(
            destination=dst,
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
            clip_w=dst.w,
            clip_h=dst.h
        ).draw_line(x0, y0, x1, y1)
