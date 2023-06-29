from .color import Palette

def simple_draw(hal):
    return SimpleDrawer(hal)


class SimpleDrawer:
    def __init__(self, hal):
        self.hal = hal

    def interpret(self, expression):
        match expression:
            case 'fill-random':
                self.hal.screen.fill(Palette.random())
                return 'ok!'
            case 'exit':
                self.hal.exit_signalled = True
                return 'bye!'
            case _:
                return f'cannot evaluate expression: `{expression}`'
