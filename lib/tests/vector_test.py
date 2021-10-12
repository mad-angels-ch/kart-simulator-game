import math
import random
from lib.vector import Vector
from lib.point import Point


def test():
    # constructeur
    v1 = Vector(1, 2)
    assert v1._x == 1 and v1._y == 2
    v2 = Vector(*v1)
    assert v2._x == 1 and v2._y == 2

    # == and !=
    assert v1 == v1
    assert Vector(2, 2) != v1
    assert Vector(3, 3) == Vector(3, 3)
    assert Vector(1, 2) == v1

    # len
    assert len(v1) == 2

    # iter
    assert [1, 2] == [i for i in v1]

    # pos and neg
    assert Vector(1, 2) == +v1
    assert Vector(-1, -2) == -v1

    # add
    assert v1 + Vector(2, -1) == Vector(3, 1)
    v2 = Vector(1, 1)
    v2 += v1
    assert v2 == Vector(2, 3)

    # sub
    assert v1 - Vector(1, 1) == Vector(0, 1)
    v2 = Vector(1, 1)
    v2 -= v1
    assert v2 == Vector(0, -1)

    # mul
    assert v1 * 2 == Vector(2, 4)
    v2 = Vector(1, 1)
    v2 *= 2
    assert v2 == Vector(2, 2)

    # item
    assert v1[0] == 1
    assert v1["x"] == 1
    assert v1["X"] == 1
    assert v1[1] == 2
    assert v1["y"] == 2
    v2 = Vector(1, 1)
    v2[0] = 2
    v2[1] = 3
    assert v2 == Vector(2, 3)
    v2["x"] = 4
    v2["y"] = 5
    assert v2 == Vector(4, 5)
    v2["X"] = -1
    assert v2 == Vector(-1, 5)

    # norm
    assert v1.norm() == math.sqrt(5)
    assert Vector(0, 0).norm() == 0
    assert Vector(-1, -1).norm() == math.sqrt(2)
    v2 = Vector(6, 8)
    v2.set_norm(5)
    assert v2 == Vector(3, 4)

    # scalarProduct
    assert v1.scalarProduct(Vector(0, 0)) == 0
    assert Vector(1, 1).scalarProduct(Vector(1, 1)) != 0
    assert Vector(1, 1).scalarProduct(Vector(1, -1)) == 0
    assert Vector(1, 1).scalarProduct(Vector(-1, 1)) == 0
    assert Vector(1, 1).scalarProduct(Vector(-1, -1)) != 0
    assert (
        Vector(1, 1).scalarProduct(Vector(-1, -1) * random.randint(0, 10000) / 10) != 0
    )

    # normalvector
    assert v2.scalarProduct(v2.normalVector()) == 0

    # isNormal/collinear
    assert v1.isNormal(Vector(0, 0))
    assert v1.isCollinear(Vector(0, 0))
    assert not v1.isCollinear(Vector(0, 1))
    assert not v1.isCollinear(Vector(1, 0))
    assert not v1.isCollinear(Vector(1, 1))
<<<<<<< HEAD
    assert not v1.isCollinear(v1.normalVector() * random.randint(0, 10000) / 10)


    # Rotation
    v3=Vector(1,0)
    v3.rotate(angle=(math.pi/2))
    # print("x:",v3[0],"y:",v3[1])
=======
    assert v1.isCollinear(v1 * random.randint(0, 10000) / 100)
    assert not v1.isCollinear(v1.normalVector() * random.randint(0, 10000) / 10)
    assert Vector(0, 0).isCollinear(v1)
    assert Vector(0, 0).isNormal(v1)

    # direction + rotation
    v2 = Vector(1, 0)
    assert v2.direction() == 0
    assert Vector(0, 1).direction() == math.pi / 2
    assert Vector(1, 1).direction() == math.pi / 4
    assert Vector(-1, 0).direction() == math.pi
    assert Vector(0, -1).direction() == math.pi / 2 * 3
    assert Vector(math.cos(1), math.sin(1)).direction() == 1
    v2.rotate(math.pi)
    assert v2.direction() == math.pi
    # v2.rotate(math.pi / 3)
    # print(v2.direction())
    # print(math.pi / 3 * 4)
    # assert v2.direction() == math.pi + math.pi / 3

    # orthogonal projection
    assert v1.orthogonalProjection(Vector(1, 0)) == Vector(1, 0)
    assert v1.orthogonalProjection(Vector(0, 1)) == Vector(0, 2)
    assert v1.orthogonalProjection(v1) == v1
    assert Vector(0, 0).orthogonalProjection(v1) == Vector(0, 0)

    # scale
    v2 = Vector(1, 7)
    v2.scaleX(3)
    assert v2 == Vector(3, 7)
    v2.scaleY(-1 / 7)
    assert v2 == Vector(3, -1)

    # fromPoints
    assert Vector.fromPoints(Point(0, 0), Point(1, 2)) == v1
    assert Vector.fromPoints(Point(*v1), Point(0, 3)) == Vector(-1, 1)
>>>>>>> bcb557e717c8ff10748d04722d6e180e9510ff00
