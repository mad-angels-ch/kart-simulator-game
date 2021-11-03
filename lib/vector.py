from logging import warning
import math


class Vector:
    precision = 1e-6

    _x: float
    _y: float

    def fromPoints(point1: "Point", point2: "Point") -> "Vector":
        return Vector(*[point2[i] - point1[i] for i in range(len(point1))])

    def __init__(self, x: float, y: float):
        self._x = x
        self._y = y

    def __len__(self) -> int:
        return 2

    def __iter__(self):
        return iter((self._x, self._y))

    def __neg__(self) -> "Vector":
        return Vector(-self._x, -self._y)

    def __pos__(self) -> "Vector":
        return self

    def __add__(self, other: "Vector") -> "Vector":
        return Vector(self._x + other._x, self._y + other._y)

    def __sub__(self, other: "Vector") -> "Vector":
        return self + (-other)

    def __mul__(self, other: float) -> "Vector":
        return Vector(self._x * other, self._y * other)

    def __truediv__(self, other: float) -> "Vector":
        return Vector(self._x / other, self._y / other)

    def __pow__(self, other: int) -> float:
        if other != 2:
            raise ValueError()
        return self.scalarProduct(self)

    def __eq__(self, o: "Vector") -> bool:
        return math.isclose(self._x, o._x, abs_tol=Vector.precision) and math.isclose(
            self._y, o._y, abs_tol=Vector.precision
        )

    def __ne__(self, o: object) -> bool:
        return not self == o

    def __getitem__(self, index: "int | str") -> float:
        if type(index) == str:
            index = index.lower()
        if index == 0 or index == "x":
            return self._x
        elif index == 1 or index == "y":
            return self._y
        else:
            raise ValueError()

    def __setitem__(self, index: "int | str", value: float) -> None:
        if type(index) == str:
            index = index.lower()
        if index == 0 or index == "x":
            self._x = value
        elif index == 1 or index == "y":
            self._y = value
        else:
            raise ValueError()

    def norm(self) -> None:
        return math.hypot(*self)

    def set_norm(self, newNorm: float) -> None:
        try:
            factor = newNorm / self.norm()
        except ZeroDivisionError:
            return
        else:
            for i in range(len(self)):
                self[i] *= factor

    def scalarProduct(self, other: "Vector") -> float:
        return self._x * other._x + self._y * other._y

    def isNormal(self, other: "Vector") -> bool:
        return math.isclose(self.scalarProduct(other), 0, abs_tol=Vector.precision)

    def isCollinear(self, other: "Vector") -> bool:
        return self.normalVector().isNormal(other)

    def normalVector(self) -> "Vector":
        return Vector(-self._y, self._x)

    def direction(self) -> float:
        """Retourne l'angle formé par ce vecteur et un vecteur de composantes 1 et 0.
        L'angle est situé entre 0 et 2 Pi"""
        angle = math.atan2(self._y, self._x)
        if angle < 0:
            angle += 2 * math.pi
        return angle

    def rotateCosSin(self, cosAngle: float, sinAngle: float):
        self._x, self._y = (
            self._x * cosAngle - self._y * sinAngle,
            self._x * sinAngle + self._y * cosAngle,
        )

    def rotate(self, angle: float) -> None:
        cos = math.cos(angle)
        sin = math.sin(angle)
        self.rotateCosSin(cos, sin)

    def orthogonalProjection(self, vector: "Vector") -> "Vector":
        "Projete CE vecteur sur le vecteur donné en paramètre"
        return vector * ((self.scalarProduct(vector)) / (vector ** 2))

    def scaleX(self, factor: float) -> None:
        "Multiplie la composante du vecteur par le facteur donné"
        self._x *= factor

    def scaleY(self, factor: float) -> None:
        "Multiplie la composante du vecteur par le facteur donné"
        self._y *= factor

    def x(self) -> float:
        return self._x

    def y(self) -> float:
        return self._y

    def get_x(self) -> float:
        warning(f"{__name__}.get_x() is deprecated, use [0] or ['x'] instead")
        return self._x

    def get_y(self) -> float:
        warning(f"{__name__}.get_y() is deprecated, use [1] or ['y'] instead")
        return self._y
