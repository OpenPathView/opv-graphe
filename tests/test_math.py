from atrevrix.graphe import get_distance, get_angle, Point


def test_distance():
    a = Point(x=48.850000, y=2.350000)  # Paris
    b = Point(x=40.716667, y=-74.000000)  # NewYork
    assert(round(get_distance(a, b), 5 == 5843114.78844))


def test_angle():
    a = Point(x=48.850000, y=2.350000)  # Paris
    b = Point(x=40.716667, y=-74.000000)  # NewYork
    c = Point(x=9.08196, y=7.402968)  # Abuja (Nigeria)
    assert(round(get_angle(a, b, c), 5) == 1.97882)
