import math
from typing import Tuple


class Vector:
    """Juste pour éviter les imports circulaires"""


class Point:
    """C'est pour créer des points"""

    precision = 1e-6

    _x: float
    _y: float

    def __init__(self, coordinates: Tuple[float, float] = (0, 0)) -> None:
        self._x = coordinates[0]
        self._y = coordinates[1]

    def __len__(self) -> int:
        """Dimension du point"""
        return 2

    def __iter__(self):
        """C'est pour les for in"""
        return iter((self._x, self._y))

    def __eq__(self, o: "Point") -> bool:
        """C'est pour les =="""
        return math.isclose(self._x, o._x, abs_tol=Point.precision) and math.isclose(
            self._y, o._y, abs_tol=Point.precision
        )

    def __ne__(self, o: object) -> bool:
        "C'est pour les !="
        return not self == o

    def __getitem__(self, index: int) -> float:
        "C'est pour les []"
        if index == 0:
            return self._x
        elif index == 1:
            return self._y
        else:
            raise ValueError()

    def __setitem__(self, index: int, value: float) -> None:
        "C'est pour les [] ="
        if index == 0:
            self._x = value
        elif index == 1:
            self._y = value
        else:
            raise ValueError()

    def __str__(self) -> str:
        """C'est pour les str() (et donc les print)"""
        return f"Point({self._x}, {self._y})"

    def translate(self, vector: "Vector") -> None:
        "Translation par le vecteur"
        for i in range(len(self)):
            self[i] += vector[i]

    def distanceOf(self, point: "Point") -> float:
        """Distance séparant les deux points"""
        return math.hypot(*[self[i] - point[i] for i in range(len(self))])

    def squareDistanceOf(self, point: "Point") -> float:
        """Carré de la distance séparant les deux points"""
        return (self[0] - point[0]) * (self[0] - point[0]) + (
            (self[1] - point[1]) * (self[1] - point[1])
        )

    def x(self) -> float:
        """Coordonné x"""
        return self[0]

    def y(self) -> float:
        """Coordonné y"""
        return self[1]

    def copy(self) -> "Point":
        """Copie le point"""
        return Point(self)
