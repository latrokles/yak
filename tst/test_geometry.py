from yak.geometry import Point, Rectangle

# gonna be a bit lazy here by testing in logical groupings
# I'm glad the blue book has a few examples to use as test cases.
def test_point_comparisons():
    assert (Point(45, 230) < Point(175, 270)) is True
    assert (Point(45, 230) < Point(175, 200)) is False
    assert (Point(45, 230) > Point(175, 200)) is False
    assert (Point(175, 270) > Point(45, 230)) is True
    assert Point(45, 230).max(Point(175, 200)) == Point(175, 230)
    assert Point(45, 230).min(Point(175, 200)) == Point(45, 200)


def test_point_arithmetic():
    assert (Point(45, 230) + Point(175, 300)) == Point(220, 530)
    assert (Point(45, 230) + 175) == Point(220, 405)
    assert (Point(45, 230) - Point(175, 300)) == Point(-130, -70)
    
    # no rational numbers :sad:
    assert (Point(160, 240) / 50) == Point(3.2, 4.8)
    assert (Point(160, 240) // 50) == Point(3, 4)
    assert (Point(160, 240) // Point(50, 50)) == Point(3, 4)
    assert abs(Point(45, 230) - Point(175, 300)) == Point(130, 70)

    # python rounding treats .5 different than smalltalk... :shrug:
    assert round(Point(120.5, 220.7)) == Point(120, 221)
    assert Point(160, 240).truncate_to(50) == Point(150, 200)


def test_point_functions():
    # The two tests below are stand-ins for the actual test
    # since floating point comparisons are so much fun. I'll
    # use a proper comparison tomorrow.
    # assert Point(45, 230).dist(Point(175, 270)) == 136.015
    # assert Point(160, 240).normal() == Point(-0.83105, 0.5547)
    assert Point(160, 240).dot_product(Point(50, 50)) == 20_000
    assert Point(160, 240).grid(Point(50, 50)) == Point(150, 250)
    assert Point(160, 240).truncated_grid(Point(50, 50)) == Point(150, 200)
    assert Point(175, 300).transpose() == Point(300, 175)


def test_point_conversions():
    assert Point(10, 10).corner(Point(50, 50)) == Rectangle(Point(10, 10), Point(50, 50))
    assert Point(10, 10).extent(Point(50, 50)) == Rectangle(Point(10, 10), Point(60, 60))

def test_rectangle_factories():
    assert Rectangle.from_sides(10, 50, 10, 50) == Rectangle(Point(10,10), Point(50, 50))
    assert Rectangle.from_coordinates_and_dimensions(50, 50, 50, 50) == Rectangle(Point(50, 50), Point(100, 100))


def test_rectangle_properties():
    r = Rectangle(Point(10, 10), Point(60, 60))
    assert r.width == 50
    assert r.height == 50
    assert r.top == 10
    assert r.right == 60
    assert r.bottom == 60
    assert r.left == 10
    assert r.top_left == Point(10, 10)
    assert r.top_center == Point(35, 10)
     