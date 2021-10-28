from typing import List
from logging import info, warning
from math import sin, cos

from lib import Point, Vector, Segment

from .Object import Object
from .Circle import Circle


class Polygon(Object):
    _vertices: List[Point]
    _angleCosSin: List[float]

    def __init__(self) -> None:
        super().__init__()
        self._vertices = list()
        self._angleCosSin = list()

    def angleCosSin(self, deltaTime: float = 0) -> List[float]:
        if not deltaTime:
            self._angleCosSin
        angle = super().angle(deltaTime=deltaTime)
        return [fun(angle) for fun in [cos, sin]]

    def updateAngleCosSin(self) -> None:
        self._angleCosSin = [fun(self.angle()) for fun in [cos, sin]]

    def set_angle(self, newAngle: float) -> None:
        super().set_angle(newAngle)
        self.updateAngleCosSin()

    def rotate(self, angle: float) -> None:
        super().rotate(angle)
        self.updateAngleCosSin()

    def rel_vertices(self) -> List[Point]:
        """Retourne la coordonnée relative des sommets,
        par rapport au centre et à l'angle"""
        return self._vertices

    def rel_vertex(self, vertexIndex: int) -> Point:
        """Retourne la coordonnée relative du sommet,
        par rapport au centre et à l'angle"""
        return self._vertices[vertexIndex]

    def abs_vertex(self, deltaTime: float = 0) -> Point:
        """Retourne la coordonnée absolue des sommets,
        en tenant compte du centre et de l'angle"""
        return [self.abs_vertex(i, deltaTime) for i in range(len(self.rel_vertices()))]

    def abs_vertex(self, vertexIndex: int, deltaTime: float = 0) -> Point:
        """Retourne la coordonnée absolue du sommet,
        en tenant compte du centre et de l'angle"""
        vertexV = Vector(*self.rel_vertex(vertexIndex))
        vertexV.rotateCosSin(*self.angleCosSin(deltaTime))
        vertexP = Point(*vertexV)
        vertexP.translate(Vector(*self.center(deltaTime)))
        return vertexP

    def collides(self, object: "Object") -> bool:
        if isinstance(object, Circle):
            second = len(self.rel_vertices()) - 1
            for first in range(len(self.rel_vertices())):
                vertex = self.abs_vertex(first)

                # collision sur un sommet
                if vertex.distanceOf(object.center()) < object.radius():
                    return True

                # collision sur un côté
                side = Segment(vertex, self.abs_vertex(second))
                projection: Point = side.orthogonalProjection(object.center())
                if side.passBy(projection):
                    if object.center().distanceOf(projection):
                        return True

                second = first

            return False

        elif isinstance(object, Polygon):
            info(
                f"{__name__}.collides() does not currently support collision between two Polygons"
            )
            return False

        else:
            return object.collides(self)
