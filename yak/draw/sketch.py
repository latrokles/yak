from dataclasses import dataclass, field

from yak.draw.color import ColorFmt
from yak.draw.fb import Framebuffer
from yak.draw.window import Mouse, Window


@dataclass
class Sketch:
    width: int
    height: int
    scale: int = 1
    color_format: ColorFmt = ColorFmt.RGBA
    title: str = ''
    window: Window = field(init=False)

    def __post_init__(self):
        self.window = Window(self.title, self.width, self.height, self.scale, self.color_format)
        self.window.register_mouse_handler(self.mouse_updated)
        self.window.open()
        self.window.run(self)

    @property
    def canvas(self) -> Framebuffer:
        return self.window.fb

    @property
    def mouse(self) -> Mouse:
        return self.window.mouse

    def setup(self) -> None:
        pass

    def draw(self) -> None:
        pass

    def exit(self) -> None:
        pass

    def mouse_updated(sel):
        pass
