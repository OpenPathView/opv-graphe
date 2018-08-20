
from atrevrix.graphe import Point
from atrevrix.graphe.point import POINT_TYPE_GPS


def test_point():
    point = Point()

    def point_test(x, y ,z , ptype):
        assert(point.x == x)
        assert (point.y == y)
        assert (point.z == z)
        assert (point.type == ptype)

    point_test(0, 0, 0, POINT_TYPE_GPS)

    point.x = 10
    point.y = 15
    point.z = 20

    point_test(10, 15, 20, POINT_TYPE_GPS)

    assert(point.is_gps() is True)

    assert(point.to_dict() == {
        "latitude": 10,
        "longitude": 15,
        "altitude": 20,
        "type": POINT_TYPE_GPS
    })

    point.latitude = 25
    point.longitude = 30
    point.altitude = 35

    assert(point.latitude == 25)
    assert (point.longitude == 30)
    assert (point.altitude == 35)

    point_test(25, 30, 35, POINT_TYPE_GPS)

    point.type = 42

    assert(point.is_gps() is False)

    point.x = 10
    point.y = 15
    point.z = 20
    
    assert(point.to_dict() == {
        "x": 10,
        "y": 15,
        "z": 20,
        "type": 42
    })

