import threading

import flask
import sdl2

from dataclasses import dataclass

from .draw.color import ColorFmt, Palette
from .draw.form import Form


YAK_2_SDL_FORMAT = {
    ColorFmt.RGBA: sdl2.SDL_PIXELFORMAT_RGBA8888,
    ColorFmt.ARGB: sdl2.SDL_PIXELFORMAT_ARGB8888,
}


def map_colorformat(yak_format: ColorFmt) -> int:
    sdl_fmt = YAK_2_SDL_FORMAT.get(yak_format)
    if sdl_fmt is None:
        raise RuntimeError(f'There is no sdl mapping for fmt={yak_format}')
    return sdl_fmt


class MachineError(Exception):
    """Raised for issues with the hal."""


class Machine:
    def __init__(self, width, height, scale, color_format, server_opts):
        self.w = width * scale
        self.h = height * scale
        self.scale = scale
        self.screen = Form(0, 0, width, height, color_format)
        self.server = EvalServer(self, server_opts)

        self.running = False
        self.exit_signalled = False

    def start(self):
        if sdl2.SDL_Init(sdl2.SDL_INIT_VIDEO) < 0:
            raise MachineError(f'Canot initialize SDL: {sdl2.SDL_Geterror()}')

        window_opts = sdl2.SDL_WINDOW_RESIZABLE | sdl2.SDL_WINDOW_BORDERLESS
        self.window = sdl2.SDL_CreateWindow(
            ''.encode('utf-8'),
            sdl2.SDL_WINDOWPOS_UNDEFINED,
            sdl2.SDL_WINDOWPOS_UNDEFINED,
            self.w,
            self.h,
            window_opts
        )

        self.renderer = sdl2.render.SDL_CreateRenderer(
            self.window,
            -1,
            sdl2.SDL_RENDERER_PRESENTVSYNC
        )

        sdl2.SDL_SetWindowMinimumSize(self.window, self.screen.w, self.screen.h)
        sdl2.render.SDL_RenderSetLogicalSize(self.renderer, self.screen.w, self.screen.h)
        sdl2.render.SDL_RenderSetIntegerScale(self.renderer, 1)

        self.texture = sdl2.SDL_CreateTexture(
            self.renderer,
            map_colorformat(self.screen.color_format),
            sdl2.SDL_TEXTUREACCESS_STREAMING,
            self.screen.w,
            self.screen.h
        )
        self.start_server()
        self.running = True
        self.run()

    def start_server(self):
        server_thread = threading.Thread(target=self.server.start, daemon=True)
        server_thread.start()

    def stop(self):
        if not self.running:
            return

        self.running = False
        sdl2.SDL_DestroyTexture(self.texture)
        sdl2.SDL_DestroyRenderer(self.renderer)
        sdl2.SDL_DestroyWindow(self.window)
        sdl2.SDL_Quit()

    def run(self):
        while self.running:
            self._handle_events()
            if self.exit_signalled:
                break

            self._redisplay()
        self.stop()

    def evaluate(self, expression):
        match expression:
            case 'fill-random':
                self.screen.fill(Palette.random())
                return 'ok!'
            case 'exit':
                self.exit_signalled = True
                return 'bye!'
            case _:
                return f'cannot evaluate expression: `{expression}`'

    def _handle_events(self):
        event = sdl2.SDL_Event()
        while sdl2.SDL_PollEvent(event) != 0:
            self._handle(event)

    def _redisplay(self):
        sdl2.SDL_UpdateTexture(
            self.texture,
            None,
            self.screen.bitmap_bytes,
            self.screen.w * self.screen.depth
        )
        sdl2.SDL_RenderClear(self.renderer)
        sdl2.SDL_RenderCopy(self.renderer, self.texture, None, None)
        sdl2.SDL_RenderPresent(self.renderer)

    def _handle(self, event):
        if event.type == sdl2.SDL_QUIT:
            self.exit_signalled = True
            return


@dataclass
class EvalServerOpts:
    host: str
    port: int


class EvalServer:
    def __init__(self, machine, opts):
        self.machine = machine
        self.host = opts.host
        self.port = opts.port
        self._http = flask.Flask(__name__)
        self._set_up_routes()

    def start(self):
        self._http.run(host=self.host, port=self.port)

    def _set_up_routes(self):
        self._http.add_url_rule('/evaluate', 'evaluate', self._evaluate, methods=['POST'])

    def _evaluate(self):
        request_dict = flask.request.json
        expression = request_dict.get('expression', '')
        evaluation_response = self.machine.evaluate(expression)
        return {'result': evaluation_response}


def launch():
    server_opts = EvalServerOpts('localhost', 45133)
    machine = Machine(320, 240, 2, ColorFmt.RGBA, server_opts)
    machine.start()
