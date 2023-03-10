from __future__ import annotations

import math
import operator

from dataclasses import dataclass


def grid(value: int|float, grid: int|float) -> int|float:
    ''' rounds to the nearest multiple of grid '''
    return ((value + (grid // 2)) // grid) * grid


def truncate_to_grid(value: int|float, grid: int|float) -> int|float:
    ''' truncates to the nearest multiple of grid '''
    return value - (value % grid)


# implements the Point protocol from the blue book (pg. 340).
@dataclass
class Point:
    x: int|float
    y: int|float

    # comparisons
    def __lt__(self, p: Point) -> bool:
        return (self.x < p.x) and (self.y < p.y)

    def __le__(self, p: Point) -> bool:
        return (self.x <= p.x) and (self.y <= p.y)

    def __gt__(self, p: Point) -> bool:
        return (self.x > p.x) and (self.y > p.y)

    def __ge__(self, p: Point) -> bool:
        return (self.x >= p.x) and (self.y >= p.y)

    def __eq__(self, p: Point) -> bool:
        return (self.x == p.x) and (self.y == p.y)

    def max(self, p: Point) -> Point:
        """Return the lower right corner of the rectangle defined by `self` and `p`."""
        return Point(max(self.x, p.x), max(self.y, p.y))

    def min(self, p: Point) -> Point:
        """Return the upper left corner of the rectangle defined by `self` and `p`."""
        return Point(min(self.x, p.x), min(self.y, p.y))

    # arithmetic
    def __mul__(self, scale: int|Point) -> Point:
        return self.__arithmetic_op(scale, operator.mul)

    def __add__(self, delta: int|Point) -> Point:
        return self.__arithmetic_op(delta, operator.add)

    def __sub__(self, delta: int|Point) -> Point:
        return self.__arithmetic_op(delta, operator.sub)

    def __truediv__(self, scale: int|Point) -> Point:
        return self.__arithmetic_op(scale, operator.truediv)

    def __floordiv__(self, scale: int|Point) -> Point:
        return self.__arithmetic_op(scale, operator.floordiv)

    def __abs__(self) -> Point:
        return Point(abs(self.x), abs(self.y))
        
    def __arithmetic_op(self, arg: int|Point, op: Callable) -> Point:
        match arg:
            case int()|float():
                return Point(op(self.x, arg), op(self.y, arg))
            case Point():
                return Point(op(self.x, arg.x), op(self.y, arg.y))
            case _:
                raise TypeError('arg must be int, float, or Point')

    # truncation and round off
    def __round__(self) -> Point:
        return Point(round(self.x), round(self.y))

    def truncate_to(self, grid: int|float) -> Point:
        return Point(truncate_to_grid(self.x, grid), truncate_to_grid(self.y, grid))

    # functions
    def dist(self, p: Point) -> int|float:
        dist_x_squared = (self.x - p.x) ** 2
        dist_y_squared = (self.y - p.y) ** 2
        return math.sqrt(dist_x_squared + dist_y_squared)

    def dot_product(self, p: Point) -> int|float:
        return (self.x * p.x) + (self.y * p.y)

    def grid(self, p: Point) -> Point:
        return Point(grid(self.x, p.x), grid(self.y, p.y))

    def normal(self) -> Point:
        n = Point(-self.y, self.x)
        d = (n.x ** 2) + (n.y ** 2)
        if d == 0:
            return Point(-1, 0)
        return n / math.sqrt(d)

    def truncated_grid(self, p: Point) -> Point:
        return Point(truncate_to_grid(self.x, p.x), truncate_to_grid(self.y, p.y))

    def transpose(self) -> Point:
        return Point(self.y, self.x)

    # conversions
    def corner(self, p: Point) -> Rectangle:
        pass

    def extent(self, p: Point) -> Rectangle:
        pass


# implements the Rectangle protocol from the blue book (pg. 344).
@dataclass
class Rectangle:
    origin: Point  # top left corner
    corner: Point  # bottom right corner

    @staticmethod
    def from_sides(left: int|float, right: int|float, top: int|float, bottom: int|float) -> Rectangle:
        return Rectangle(Point(left, top), Point(right, bottom))

    @staticmethod
    def from_point_with_extent(origin: Point, extent: Point) -> Rectangle:
        return Rectangle(origin, origin + extent)

    @staticmethod
    def from_coordinates_and_dimensions(x: int|float, y: int|float, width: int|float, height: int|float) -> Rectangle:
        # handle negative width and/or height
        # - recompute origin ?
        # - raise error to avoid degenerate triangle?
        origin = Point(x, y)
        return Rectangle(origin, origin + Point(width, height)) 

    # properties
    @property
    def width(self) -> int|float:
        return corner.x - origin.x

    @property
    def height(self) -> int|float:
        return corner.y - origin.y

    @property
    def extent(self) -> Point:
        return self.corner - self.origin

    @property
    def top(self) -> int|float:
        return self.origin.y

    @property
    def right(self) -> int|float:
        return self.corner.x

    @property
    def bottom(self) -> int|float:
        return self.corner.y

    @property
    def left(self) -> int|float:
        return self.origin.x
    
    @property
    def center(self) -> Point:
        return Point(self.origin - self.corner) // 2

    @property
    def top_left(self) -> Point:
        return self.origin

    @property
    def top_center(self) -> Point:
        return Point(self.center.x, self.top)

    @property
    def top_right(self) -> Point:
        return Point(self.right, self.top)

    @property
    def right_center(self) -> Point:
        return Point(self.right, self.center.y)

    @property
    def bottom_right(self) -> Point:
        return self.corner

    @property
    def bottom_center(self) -> Point:
        return Point(self.center.x, self.bottom)

    @property
    def bottom_left(self) -> Point:
        return Point(self.left, self.bottom)

    @property
    def left_center(self) -> Point:
        return Point(self.left, self.center.y)
