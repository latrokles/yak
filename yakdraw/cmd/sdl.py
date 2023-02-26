import ctypes
import sdl2
import sys


from yakdraw.color import ColorFmt, Palette
from yakdraw.fb import Framebuffer


WIN_WIDTH = 640
WIN_HEIGHT = 480

FB_WIDTH = 320
FB_HEIGHT = 240

def test():
    # ignoring all sdl errors here

    sdl2.SDL_Init(sdl2.SDL_INIT_VIDEO)

    window = sdl2.SDL_CreateWindow('sdltest'.encode('utf-8'),
                                   sdl2.SDL_WINDOWPOS_UNDEFINED,
                                   sdl2.SDL_WINDOWPOS_UNDEFINED,
                                   WIN_WIDTH,
                                   WIN_HEIGHT,
                                   0)
    
    renderer = sdl2.render.SDL_CreateRenderer(window,
                                              -1,
                                              sdl2.SDL_RENDERER_PRESENTVSYNC)

    sdl2.SDL_SetWindowMinimumSize(window, FB_WIDTH, FB_HEIGHT)

    sdl2.render.SDL_RenderSetLogicalSize(renderer, FB_WIDTH, FB_HEIGHT)
    sdl2.render.SDL_RenderSetIntegerScale(renderer, 1)

    texture = sdl2.SDL_CreateTexture(renderer,
                                     sdl2.SDL_PIXELFORMAT_RGBA8888,
                                     sdl2.SDL_TEXTUREACCESS_STREAMING,
                                     FB_WIDTH,
                                     FB_HEIGHT)

    fb = Framebuffer(FB_WIDTH, FB_HEIGHT, ColorFmt.RGBA)
    for y in range(FB_HEIGHT):
        for x in range(FB_WIDTH):
            fb.put_pixel(x, y, Palette.WHITE)

    while True:        
        event = sdl2.SDL_Event()
        while sdl2.SDL_PollEvent(event) != 0:
            if event.type == sdl2.SDL_QUIT:
                sys.exit(0)

            if event.type == sdl2.SDL_MOUSEBUTTONDOWN:
                x = event.button.x
                y = event.button.y

                fb.put_pixel(x, y, Palette.BLUE1)
         
        # copy framebuffer to texture and render it in sdl window

        # 1. copy framebuffer into texture
        sdl2.SDL_UpdateTexture(texture, None, fb.memory(), FB_WIDTH * 4)

        # 2. display the texture in sdl window
        sdl2.SDL_RenderClear(renderer)
        sdl2.SDL_RenderCopy(renderer, texture, None, None)
        sdl2.SDL_RenderPresent(renderer)