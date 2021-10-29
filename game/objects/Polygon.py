from typing import List
from logging import info
from math import sin, cos

import lib

from .Object import Object
from .Circle import Circle


class Polygon(Object):
    _vertices: List[lib.Point]
    _angleCosSin: List[float]
    _convex: bool

    def __init__(self) -> None:
        super().__init__()
        self._vertices = list()
        self._angleCosSin = list()

    def __len__(self) -> int:
        return len(self._vertices)

    def convex(self) -> bool:
        """Retourne True si le polygon est convexe"""
        return self._convex

    def updateAngleCosSin(self) -> None:
        self._angleCosSin = [fun(self.angle()) for fun in [cos, sin]]

    def angleCosSin(self, deltaTime: float = 0) -> List[float]:
        if not deltaTime:
            self._angleCosSin
        angle = super().angle(deltaTime=deltaTime)
        return [fun(angle) for fun in [cos, sin]]

    def set_angle(self, newAngle: float) -> None:
        super().set_angle(newAngle)
        self.updateAngleCosSin()

    def rotate(self, angle: float) -> None:
        super().rotate(angle)
        self.updateAngleCosSin()

    def vertex(self, vertexIndex: int, deltaTime: float = 0) -> lib.Point:
        vertexV = lib.Vector(*self.rel_vertex(vertexIndex))
        vertexV.rotateCosSin(*self.angleCosSin(deltaTime))
        vertex = lib.Point(*vertexV)
        vertex.translate(lib.Vector(*self.center(deltaTime)))
        return vertex

    def vertices(self, deltaTime: float = 0) -> List[lib.Point]:
        return [self.vertex(i, deltaTime) for i in range(len(self))]

    def rel_vertices(self) -> List[lib.Point]:
        """Retourne la coordonnée relative des sommets,
        par rapport au centre et à l'angle"""
        return self._vertices

    def rel_vertex(self, vertexIndex: int) -> lib.Point:
        """Retourne la coordonnée relative du sommet,
        par rapport au centre et à l'angle"""
        return self._vertices[vertexIndex]

    def abs_vertex(self, deltaTime: float = 0) -> lib.Point:
        """Retourne la coordonnée absolue des sommets,
        en tenant compte du centre et de l'angle"""
        return [self.abs_vertex(i, deltaTime) for i in range(len(self.rel_vertices()))]

    def abs_vertex(self, vertexIndex: int, deltaTime: float = 0) -> lib.Point:
        """Retourne la coordonnée absolue du sommet,
        en tenant compte du centre et de l'angle"""
        vertexV = lib.Vector(*self.rel_vertex(vertexIndex))
        vertexV.rotateCosSin(*self.angleCosSin(deltaTime))
        vertexP = lib.Point(*vertexV)
        vertexP.translate(lib.Vector(*self.center(deltaTime)))
        return vertexP

    def collides(self, other: "Object", timeInterval: float) -> bool:
        if isinstance(other, Circle):
            newSelf = lib.Polygon(*self.vertices(timeInterval))
            newOther = lib.Circle(other.center(timeInterval), other.radius())
            if newSelf.collides(newOther):
                return True

            # contrôller que les objets ne se sont pas passés par dessus
            # À compléter ...
            return False

        elif isinstance(other, Polygon):
            newSelf = lib.Polygon(*self.vertices(timeInterval))
            newOther = lib.Polygon(*other.vertices(timeInterval))
            if newSelf.collides(newOther):
                return True

            # contrôller que les polygones ne se sont pas passés par dessus
            # À compléter ...
            return False

        else:
            return other.collides(self)

    def collisionPoint(self, other: "Object") -> lib.Point:
        # à compléter
        return super().collisionPoint(other)

    def collisionTangent(self, other: "Object") -> lib.Vector:
        # à compléter
        return super().collisionTangent(other)
