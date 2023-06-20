import dataclasses
import sdl2

from typing import Callable

from yak.draw.color import ColorFmt
from yak.draw.fb import Framebuffer


YAK_2_SDL_FORMAT = {
    ColorFmt.RGBA: sdl2.SDL_PIXELFORMAT_RGBA8888,
    ColorFmt.ARGB: sdl2.SDL_PIXELFORMAT_ARGB8888,
}


def map_colorformat(yak_format: ColorFmt) -> int:
    sdl_fmt = YAK_2_SDL_FORMAT.get(yak_format)
    if sdl_fmt is None:
        raise RuntimeError(f'There is no sdl mapping for fmt={yak_format}')
    return sdl_fmt


@dataclasses.dataclass
class Mouse:
    x: int = 0
    y: int = 0
    px: int = 0
    py: int = 0
    left: bool = False
    middle: bool = False
    right: bool = False

    def move(self, x: int, y: int) -> None:
        self.px, self.py = self.x, self.y
        self.x, self.y = x, y

    def moved(self) -> bool:
        return self.x, self.y != self.px, self.py


class Window:
    def __init__(self, title: str, width: int, height: int, scale: int, color_format: ColorFmt):
        self.title = title
        self.w = width * scale
        self.h = height * scale
        self.scale = scale
        self.fb = Framebuffer(width, height, color_format)

        self.win = None
        self.renderer = None
        self.texture = None

        self.mouse = Mouse()

        self.active = False
        self.exit_signalled = False
        self.mouse_handlers = []

    def register_mouse_handler(self, handler: Callable[[Mouse], None]) -> None:
        self.mouse_handlers.append(handler)

    def open(self) -> None:
        if sdl2.SDL_Init(sdl2.SDL_INIT_VIDEO) < 0:
            raise RuntimeError(f'Cannot initialize SDL: {sdl2.SDL_GetError()}')

        self.win = sdl2.SDL_CreateWindow(self.title.encode('utf-8'),
                                         sdl2.SDL_WINDOWPOS_UNDEFINED,
                                         sdl2.SDL_WINDOWPOS_UNDEFINED,
                                         self.w,
                                         self.h,
                                         0)

        self.renderer = sdl2.render.SDL_CreateRenderer(self.win,
                                                       -1,
                                                       sdl2.SDL_RENDERER_PRESENTVSYNC)

        sdl2.SDL_SetWindowMinimumSize(self.win, self.fb.w, self.fb.h)
        sdl2.render.SDL_RenderSetLogicalSize(self.renderer, self.fb.w, self.fb.h)
        sdl2.render.SDL_RenderSetIntegerScale(self.renderer, 1)

        self.texture = sdl2.SDL_CreateTexture(self.renderer,
                                              map_colorformat(self.fb.fmt),
                                              sdl2.SDL_TEXTUREACCESS_STREAMING,
                                              self.fb.w,
                                              self.fb.h)
        self.active = True

    def run(self, sketch) -> None:
        sketch.setup()
        while self.active:
            self._handle_events()
            if self.exit_signalled:
                break

            sketch.draw()
            self._render()
        sketch.exit()
        self.close()

    def close(self) -> None:
        if not self.active:
            return

        sdl2.SDL_DestroyTexture(self.texture)
        sdl2.SDL_DestroyRenderer(self.renderer)
        sdl2.SDL_DestroyWindow(self.win)
        sdl2.SDL_Quit()

    def _handle_events(self) -> None:
        event = sdl2.SDL_Event()
        while sdl2.SDL_PollEvent(event) != 0:
            self._handle_event(event)

    def _render(self) -> None:
        sdl2.SDL_UpdateTexture(self.texture, None, self.fb.memory, self.fb.w * self.fb.depth)
        sdl2.SDL_RenderClear(self.renderer)
        sdl2.SDL_RenderCopy(self.renderer, self.texture, None, None)
        sdl2.SDL_RenderPresent(self.renderer)

    def _handle_event(self, event: sdl2.SDL_Event) -> None:
        if event.type == sdl2.SDL_QUIT:
            self.exit_signalled = True
            return

        if event.type == sdl2.SDL_MOUSEBUTTONDOWN:
            self._mouse_down(event.button.button)
            self._signal_mouse_event()
            return

        if event.type == sdl2.SDL_MOUSEBUTTONUP:
            self._mouse_up(event.button.button)
            self._signal_mouse_event()
            return

        if event.type == sdl2.SDL_MOUSEMOTION:
            self._mouse_moved(event.motion.x, event.motion.y)
            self._signal_mouse_event()
            return

    def _mouse_down(self, button: int) -> None:
        if button == 1:
            self.mouse.left = True
            return

        if button == 2:
            self.mouse.middle = True
            return

        if button == 3:
            self.mouse.right = True

    def _mouse_up(self, button: int) -> None:
        if button == 1:
            self.mouse.left = False
            return

        if button == 2:
            self.mouse.middle = False
            return

        if button == 3:
            self.mouse.right = False

    def _mouse_moved(self, x: int, y: int) -> None:
        self.mouse.move(x, y)

    def _signal_mouse_event(self) -> None:
        for handler in self.mouse_handlers:
             handler()
