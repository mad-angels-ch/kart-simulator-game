from typing import Iterable, List

from .point import Point
from .vector import Vector
from .Line import Line
from .Segment import Segment


class Polygon:
    _vertices: List[Point]

    def __init__(self, *vertices: Point) -> None:
        self._vertices = [Point(*vertex) for vertex in vertices]

    def __len__(self) -> int:
        return len(self._vertices)

    def vertex(self, vertexIndex: int) -> Point:
        return self._vertices[vertexIndex]

    def vertices(self) -> List[Point]:
        return self._vertices

    def edge(self, startVertexIndex: int) -> Segment:
        return Segment(self.vertex(startVertexIndex), self.vertex(startVertexIndex - 1))

    def edges(self) -> List[Segment]:
        return [self.edge(i) for i in range(len(self))]