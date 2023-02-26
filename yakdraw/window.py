import sdl2

from yakdraw.color import ColorFmt, Palette
from yakdraw.fb import Framebuffer


YAK_2_SDL_FORMAT = {
    ColorFmt.RGBA: sdl2.SDL_PIXELFORMAT_RGBA8888,
    ColorFmt.ARGB: sdl2.SDL_PIXELFORMAT_ARGB8888,
}


class Window:
    def __init__(self, title: str, width: int,height: int, scaling: int = 1):
        self.title = title
        self.w = width
        self.h = height
        self.scale = scaling
        self.fb = Framebuffer(self.w // self.scale,
                              self.h // self.scale,
                              ColorFmt.RGBA)

        self.win = None
        self.renderer = None
        self.texture = None

        self.active = False
        self.exit_signalled = False

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
                                              YAK_2_SDL_FORMAT.get(self.fb.fmt),
                                              sdl2.SDL_TEXTUREACCESS_STREAMING,
                                              self.fb.w,
                                              self.fb.h)
        self.active = True
        self.run()

    def run(self) -> None:
        # TODO remove this fill after we can write programs that reuse this
        for y in range(self.fb.h):
            for x in range(self.fb.w):
                self.fb.put_pixel(x, y, Palette.WHITE)
 
        while self.active:
            self._handle_events()
            if self.exit_signalled:
                break

            self._render()
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
        sdl2.SDL_UpdateTexture(self.texture, None, self.fb.memory(), self.fb.w * self.fb.depth)
        sdl2.SDL_RenderClear(self.renderer)
        sdl2.SDL_RenderCopy(self.renderer, self.texture, None, None)
        sdl2.SDL_RenderPresent(self.renderer)

    def _handle_event(self, event: sdl2.SDL_Event) -> None:
        if event.type == sdl2.SDL_QUIT:
            self.exit_signalled = True
            return

        if event.type in (sdl2.SDL_MOUSEBUTTONUP, sdl2.SDL_MOUSEBUTTONDOWN):
            self._on_mouse_button_action(event.button)
            return

        if event.type == sdl2.SDL_MOUSEMOTION:
            self._on_mouse_motion(event.motion)
            return

    def _on_mouse_button_action(self, mouse: sdl2.events.SDL_Event) -> None:
        pass

    def _on_mouse_motion(self, mouse: sdl2.events.SDL_Event) -> None:
        if mouse.state == sdl2.SDL_PRESSED:
            # this is a stand-in for now...
            # TODO replace when we can register handlers
            x, y = mouse.x, mouse.y
            self.fb.put_pixel(x, y, Palette.BLUE1)
