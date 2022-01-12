from logging import warning
import math
from typing import Tuple


class Point:
    """Juste pour éviter les imports circulaires"""


class Vector:
    precision = 1e-6

    def fromPoints(point1: Point, point2: Point) -> "Vector":
        """Créé le vecteur qui va de point1 à point2"""
        return Vector([point2[i] - point1[i] for i in range(len(point1))])

    _x: float
    _y: float

    _norm: float
    _normUptodate: bool

    def __init__(self, components: Tuple[float, float] = (0, 0)) -> None:
        self._x = components[0]
        self._y = components[1]
        self._normUptodate = False

    def __bool__(self) -> bool:
        """Pour bool(), not etc"""
        return self != Vector()

    def __len__(self) -> int:
        """Dimension du vecteur"""
        return 2

    def __iter__(self):
        """Pour les for in"""
        return iter((self._x, self._y))

    def __neg__(self) -> "Vector":
        """Pour le - (signe)"""
        return Vector((-self._x, -self._y))

    def __pos__(self) -> "Vector":
        """Pour le + (signe)"""
        return self

    def __add__(self, other: "Vector") -> "Vector":
        """Pour le + (addition)"""
        return Vector((self._x + other._x, self._y + other._y))

    def __sub__(self, other: "Vector") -> "Vector":
        """Pour le - (soustraction)"""
        return self + (-other)

    def __mul__(self, other: float) -> "Vector":
        """Pour le *"""
        return Vector((self._x * other, self._y * other))

    def __truediv__(self, other: float) -> "Vector":
        """Pour le /"""
        return Vector((self._x / other, self._y / other))

    def __pow__(self, other: int) -> float:
        """Pour le **"""
        if other != 2:
            raise ValueError("Only **2 is supported")
        return self.scalarProduct(self)

    def __eq__(self, o: "Vector") -> bool:
        """Pour le =="""
        return math.isclose(self._x, o._x, abs_tol=self.precision) and math.isclose(
            self._y, o._y, abs_tol=self.precision
        )

    def __ne__(self, o: object) -> bool:
        """Pour le !="""
        return not self == o

    def __getitem__(self, index: int) -> float:
        """Pour le []"""
        if index == 0:
            return self._x
        elif index == 1:
            return self._y
        else:
            raise ValueError()

    def __setitem__(self, index: int, value: float) -> None:
        """Pour le [] ="""
        if index == 0:
            self._x = value
        elif index == 1:
            self._y = value
        else:
            raise ValueError()
        self._normUptodate = False

    def norm(self) -> None:
        """Pour la norme"""
        if not self._normUptodate:
            self._norm = math.hypot(*self)
            self._normUptodate = True
        return self._norm

    def set_norm(self, newNorm: float) -> None:
        """Change la norme (et donc les composantes)"""
        try:
            factor = newNorm / self.norm()
        except ZeroDivisionError:
            return
        else:
            for i in range(len(self)):
                self[i] *= factor
            self._norm *= factor

    def scalarProduct(self, other: "Vector") -> float:
        """Pour le produit scalaire"""
        return self._x * other._x + self._y * other._y

    def isNormal(self, other: "Vector") -> bool:
        """Vrai si ils sont perpendiculaires"""
        return math.isclose(self.scalarProduct(other), 0, abs_tol=self.precision)

    def isCollinear(self, other: "Vector") -> bool:
        """Vrai si ils sont collinéaires"""
        return self.normalVector().isNormal(other)

    def normalVector(self) -> "Vector":
        """Un vecteur normal"""
        return Vector((-self._y, self._x))

    def direction(self) -> float:
        """L'angle formé par avec le vecteur de composantes 1 et 0.
        L'angle est situé entre 0 et 2 Pi"""
        angle = math.atan2(self._y, self._x)
        if angle < 0:
            angle += 2 * math.pi
        return angle

    def rotateCosSin(self, cosAngle: float, sinAngle: float):
        """Pour les rotations avec les cos et sin déjà calculés"""
        self._x, self._y = (
            self._x * cosAngle - self._y * sinAngle,
            self._x * sinAngle + self._y * cosAngle,
        )
        self._normUptodate = False

    def rotate(self, angle: float) -> None:
        """Pour les rotations avec les cos et sin pas encore calculés"""
        cos = math.cos(angle)
        sin = math.sin(angle)
        self.rotateCosSin(cos, sin)

    def orthogonalProjection(self, vector: "Vector") -> "Vector":
        "Projete CE vecteur sur le vecteur donné en paramètre"
        return vector * ((self.scalarProduct(vector)) / (vector ** 2))

    def scaleX(self, factor: float) -> None:
        "Multiplie la composante x par le facteur donné"
        self._x *= factor
        self._normUptodate = False

    def scaleY(self, factor: float) -> None:
        "Multiplie la composante y par le facteur donné"
        self._y *= factor
        self._normUptodate = False

    def x(self) -> float:
        """Composante x"""
        return self._x

    def y(self) -> float:
        """Composante y"""
        return self._y

    def copy(self) -> "Vector":
        """Copie le vecteur"""
        return Vector(self)

    def CosAngleBetweenTwoVectors(self, other: "Vector") -> float:
        "Le cosinus de l'angle aigu ou optu entre ce vecteur et un autre vecteur donné"
        return self.scalarProduct(other) / self.norm() * other.norm()

    def unitVector(self) -> "Vector":
        "Vecteur unitaire"
        return self / self.norm()
