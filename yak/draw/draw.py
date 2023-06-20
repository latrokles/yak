import math

from yak.draw.color import Color
from yak.draw.fb import Framebuffer
from yak.draw.geometry import Point


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


def draw_rect(fb: Framebuffer, x: int, y: int, w: int, h: int, color: Color) -> None:
    draw_line(fb, x, y, x + w, y, color)
    draw_line(fb, x, y, x, y + h, color)
    draw_line(fb, x + w, y + h, x + w, y, color)
    draw_line(fb, x + w, y + h, x, y + h, color)


def draw_circle(fb: Framebuffer, center_x: int, center_y: int, r: int, color: Color) -> None:
    angle = 0
    step = 2 * math.pi / 100

    px = x = int(center_x + (r * math.cos(angle)))
    py = y = int(center_y - (r * math.sin(angle)))

    while angle <= (2 * math.pi):
        px, py = x, y
        x = int(center_x + (r * math.cos(angle)))
        y = int(center_y - (r * math.sin(angle)))
        angle += step
        draw_line(fb, px, py, x, y, color)


def draw_polygon(fb: Framebuffer, points: list[Point], color: Color) -> None:
    if len(points) < 3:
        # should this raise an error?
        return

    prev = points[0]
    for curr in points[1:]:
        draw_line(fb, prev.x, prev.y, curr.x, curr.y, color)
        prev = curr
    # close the polygon
    draw_line(fb, points[0].x, points[0].y, points[-1].x, points[-1].y, color)


def draw_triangle(fb: Framebuffer, x0: int, y0: int, x1: int, y1: int, x2: int, y2: int, color: Color) -> None:
    draw_polygon(fb, [Point(x0, y0), Point(x1, y1), Point(x2, y2)], color)


def fill_rect(fb: Framebuffer, x: int, y: int, w: int, h: int, color: Color) -> None:
    for y0 in range(y, y + h):
        for x0 in range(x, x + w):
            draw_point(fb, x0, y0, color)


def background(fb: Framebuffer, color: Color) -> None:
    fill_rect(fb, 0, 0, fb.w, fb.h, color)
