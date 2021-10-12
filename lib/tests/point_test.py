import math
import random
from lib.point import Point


def test():
    #constructor
    p1 = Point(1, 2)
    assert p1._x == 1
    assert p1._y == 2
    p2 = Point(3, 4)
    assert p2._x == 3 and p2._y == 4
    assert p1._x == 1 and p1._y == 2

    #len + iter
    assert len(p1) == 2
    assert [1, 2] == [i for i in p1]
    assert [3, 4] == [i for i in p2]

    # == + !=
    assert p1 == Point(1, 2)
    assert p2 != p1
    assert not p1 == Point(0, 0)

    # []
    assert p1[0] == 1
    assert p1["x"] != 2
    assert p1[1] == 2
    assert not p1["Y"] != 2
    p2[0], p2["y"] = p2["Y"], p2[0]
    assert p2 == Point(4, 3)