from typing import Iterable, List

from .point import Point
from .vector import Vector
from .Line import Line
from .Segment import Segment
from .Shape import Shape
from .Circle import Circle


class Polygon(Shape):
    _vertices: List[Point]

    def __init__(self, *vertices: Point) -> None:
        self._vertices = [vertex for vertex in vertices]

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

    def collides(self, other: Shape) -> bool:
        if isinstance(other, Circle):
            second = len(self) - 1
            for first in range(len(self)):

                # collision sur un sommet
                if other.center().distanceOf(self.vertex(first)) <= other.radius():
                    return True

                # collision sur un côté
                side = Segment(self.vertex(first), self.vertex(second))
                try:
                    projection: Point = side.orthogonalProjection(other.center())
                    if side.passBy(projection):
                        if other.center().distanceOf(projection) < other.radius():
                            return True
                finally:
                    second = first

            return False

        elif isinstance(other, Polygon):
            otherEdges = other.edges()
            for selfEge in self.edges():
                for otherEdge in otherEdges:
                    if selfEge.intercepts(otherEdge):
                        return True
            return False

        else:
            return other.collides(self)
