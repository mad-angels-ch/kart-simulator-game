from .Point import Point
from .Vector import Vector
from .Line import Line
from .Segment import Segment


class Shape:
    def copy(self) -> "Shape":
        """Retourne une copie"""
        pass

    def collides(self, other: "Shape") -> bool:
        pass
