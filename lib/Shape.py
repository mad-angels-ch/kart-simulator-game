from .point import Point
from .vector import Vector
from .Line import Line
from .Segment import Segment


class Shape:
    def translate(self, vector: Vector) -> None:
        pass

    def collides(self, other: "Shape") -> bool:
        pass
