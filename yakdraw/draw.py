from yakdraw.color import Color
from yakdraw.fb import Framebuffer


def draw_point(fb: Framebuffer, x: int, y: int, color: Color):
    fb.put_pixel(x, y, color)


def draw_line(fb: Framebuffer, x0: int, y0: int, x1: int, y1: int, color: Color):
    dx = x1 - x0
    dy = y1 - y0

    x_step, y_step = 0, 0
    if dy < 0:
        dy = -dy
        y_step = -1
    else:
        y_step = 1

    if dx < 0:
        dx = -dx
        x_step = -1
    else:
        x_step = 1

    dy = 2 * dy
    dx = 2 * dx

    draw_point(fb, x0, y0, color)
    if dx > dy:
        fraction = 2 * dy - dx
        while x0 != x1:
            if fraction >= 0:
                y0 += y_step
                fraction -= dx

            x0 += x_step
            fraction += dy
            draw_point(fb, x0, y0, color)

    else:
        fraction = 2 * dx - dy
        while y0 != y1:
            if fraction >= 0:
                x0 += x_step
                fraction -= dy

            y0 += y_step
            fraction += dx
            draw_point(fb, x0, y0, color)