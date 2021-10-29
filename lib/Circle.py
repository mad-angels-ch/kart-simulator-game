from typing import Iterable, List

from .point import Point
from .vector import Vector
from .Line import Line
from .Segment import Segment
from .Shape import Shape


class Circle:
    _center: Point
    _radius: float

    def __init__(self, center: Point, radius: float) -> None:
        self._center = center
        self._radius = radius

    def center(self) -> Point:
        return self._center

    def radius(self) -> float:
        return self._radius

    def translate(self, vector: Vector) -> None:
        self._center.translate(vector)

    def collides(self, other: Shape) -> bool:
        if isinstance(other, Circle):
            return (
                self.center().distanceOf(other.center())
                <= self.radius() + other.radius()
            )

        else:
            return other.collides(self)
