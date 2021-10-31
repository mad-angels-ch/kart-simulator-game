import math
from typing import List, Tuple
from logging import info
from math import sin, cos

import lib
from lib.Segment import Segment
from lib.point import Point
from lib.vector import Vector

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
        vertexV = lib.Vector(*self._vertices[vertexIndex])
        vertexV.rotateCosSin(*self.angleCosSin(deltaTime))
        vertex = lib.Point(*vertexV)
        vertex.translate(lib.Vector(*self.center(deltaTime)))
        return vertex

    def vertices(self, deltaTime: float = 0) -> List[lib.Point]:
        return [self.vertex(i, deltaTime) for i in range(len(self))]

    def edge(self, startVertexIndex: int, deltaTime: float = 0) -> lib.Segment:
        endVertexIndex = startVertexIndex + 1
        if endVertexIndex == len(self):
            endVertexIndex = 0
        return lib.Segment(
            self.vertex(startVertexIndex, deltaTime),
            self.vertex(endVertexIndex, deltaTime),
        )

    def edges(self, deltaTime: float = 0) -> List[lib.Segment]:
        edges = []
        vertices = self.vertices(deltaTime)
        second = len(vertices) - 1
        for first in range(len(vertices)):
            edges.append(lib.Segment(vertices[first], vertices[second]))
        return edges

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

    def collisionPointAndTangent(self, other: "Object") -> Tuple[lib.Point, lib.Vector]:
        if isinstance(other, Circle):
            smallestVertexSquareDistance = math.inf
            smallestEdgeSquareDistance = math.inf
            second = len(self) - 1
            for first in range(len(self)):
                firstVertex = self.vertex(first)
                vertexSquareDistance = other.center().squareDistanceOf(firstVertex)
                if vertexSquareDistance < smallestVertexSquareDistance:
                    smallestVertexSquareDistance = vertexSquareDistance
                    nearestVertex = firstVertex

                edge = lib.Segment(firstVertex, self.vertex(second))
                projection: Point = edge.orthogonalProjection(other.center())
                if edge.passBy(projection):
                    edgeSquareDistance = other.center().squareDistanceOf(projection)
                    if edgeSquareDistance < smallestEdgeSquareDistance:
                        smallestEdgeSquareDistance = edgeSquareDistance
                        nearestEdge = edge
                        nearestProjection = projection

                second = first
            if smallestEdgeSquareDistance < smallestVertexSquareDistance:
                return nearestProjection, nearestEdge.vector()
            else:
                return (
                    nearestVertex,
                    Vector.fromPoints(other.center(), nearestVertex).normalVector(),
                )

        elif isinstance(other, Polygon):

            def findNearest(
                edges: List[lib.Segment], vertices: List[lib.Point]
            ) -> Tuple[float, lib.Point, lib.Vector]:
                smallestSquareDistance = math.inf
                for edge in edges:
                    for vertex in vertices:
                        projection: Point = edge.orthogonalProjection(vertex)
                        if edge.passBy(projection):
                            squareDistance = vertex.squareDistanceOf(projection)
                            if squareDistance < smallestSquareDistance:
                                smallestSquareDistance = squareDistance
                                nearestVertex = vertex
                                nearestEdge = edge
                return smallestSquareDistance, nearestVertex, nearestEdge.vector()

            nearests = (
                findNearest(self.edges(), other.vertices()),
                findNearest(other.edges(), self.vertices()),
            )
            nearest = 0
            if nearests[1][0] < nearests[0][0]:
                nearest = 1
            return nearests[nearest][1], nearests[nearest][2]

        else:
            return other.collisionPointAndTangent(self)
