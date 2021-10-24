import math


class Point:
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
        return self._x == o._x and self._y == o._y

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

    def x(self) -> float:
        "Obsolète, utiliser self[0] ou self['x']"
        return self._x

    def y(self) -> float:
        "Obsolète, utiliser self[1] ou self['y']"
        return self._y

    def get_x(self) -> float:
        "Obsolète, utiliser self[0] ou self['x']"
        return self._x

    def get_y(self) -> float:
        "Obsolète, utiliser self[1] ou self['y']"
        return self._y
