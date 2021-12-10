from typing import List

from .Point import Point
from .Vector import Vector
from .Line import Line
from .Segment import Segment
from .Polygon import Polygon
from .ConvexPolygon import ConvexPolygon


class Rectangle(ConvexPolygon):
    def __init__(self, v0: Point, v1: Point, v2: Point) -> None:
        v3 = Point(v2)
        v3.translate(Vector.fromPoints(v1, v0))
        super().__init__(v0, v1, v2, v3)

    def copy(self) -> "Rectangle":
        return Rectangle(*[self.vertex(i) for i in range(3)])

    def _edgesNeededForSAT(self) -> List[Segment]:
        return [self.edge(i) for i in range(2)]
