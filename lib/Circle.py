from typing import Iterable, List

from .Point import Point
from .Vector import Vector
from .Line import Line
from .Segment import Segment
from .Shape import Shape


class Circle(Shape):
    """Cercle géométrique"""
    _center: Point
    _radius: float

    def __init__(self, center: Point, radius: float) -> None:
        self._center = center
        self._radius = radius

    def copy(self) -> "Circle":
        return Circle(self.center().copy(), self.radius())

    def center(self) -> Point:
        """NE PAS MODIFIER\n
        Centre du cercle."""
        return self._center

    def radius(self) -> float:
        """Rayon du cercle."""
        return self._radius

    def translate(self, vector: Vector) -> None:
        """Translation du cercle,"""
        self._center.translate(vector)

    def collides(self, other: Shape) -> bool:
        if isinstance(other, Circle):
            return (
                self.center().distanceOf(other.center())
                <= self.radius() + other.radius()
            )

        else:
            return other.collides(self)
