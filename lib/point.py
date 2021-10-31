from logging import warning
import math


class Point:
    precision = 1e-6

    _x: float
    _y: float

    def __init__(self, x: float, y: float) -> None:
        self._x = x
        self._y = y

    def __len__(self) -> int:
        return 2

    def __iter__(self):
        return iter((self._x, self._y))

    def __eq__(self, o: "Point") -> bool:
        return math.isclose(self._x, o._x, abs_tol=Point.precision) and math.isclose(
            self._y, o._y, abs_tol=Point.precision
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

    def __str__(self) -> str:
        return f"Point({self._x}, {self._y})"

    def translate(self, vector: "Vector") -> None:
        for i in range(len(self)):
            self[i] += vector[i]

    def distanceOf(self, point: "Point") -> float:
        """Retourne la distance séparent les deux points"""
        return math.hypot(*[self[i] - point[i] for i in range(len(self))])

    def squareDistanceOf(self, point: "Point") -> float:
        """Retourne le carré de la distance séparent les deux points"""
        return (self[0] - point[0]) ** 2 + (self[1] - point[1]) ** 2

    def x(self) -> float:
        return self[0]

    def y(self) -> float:
        return self[1]

    def get_x(self) -> float:
        warning(f"{__name__}.get_x() is deprecated, use [0] or ['x'] instead")
        return self[0]

    def get_y(self) -> float:
        warning(f"{__name__}.get_y() is deprecated, use [1] or ['y'] instead")
        return self[1]
