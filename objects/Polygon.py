import math
from typing import Dict, List, Tuple
from logging import info
from math import sin, cos
import time

import lib
from lib.Point import Point

from .Object import Object
from .Circle import Circle


class Polygon(Object):
    """Classe des polygones."""

    counter = 0
    precision = 1e-6

    _vertices: List[lib.Vector]

    # Pour des questions de performance, nous stockons les valeurs des sin et cos d'angles fréquents
    _angleCosSin: List[float]
    _angleCosSin2: List[float]
    _angleCosSin2Angle: float
    _convex: bool

    def fromMinimalDict(obj: dict) -> dict:
        dic = Object.fromMinimalDict(obj)
        dic.update({"vertices": [lib.Vector(v) for v in obj["vertices"]]})
        return dic

    def __init__(self, **kwargs) -> None:
        super().__init__(**kwargs)
        self._vertices = kwargs.get(
            "vertices",
            [
                lib.Vector((math.cos(angle), math.sin(angle)))
                for angle in [0, math.pi * 2 / 3, math.pi * 4 / 3]
            ],
        )
        self.updateAngleCosSin()
        self._angleCosSin2Angle = self.angle()
        self._angleCosSin2 = self._angleCosSin

    def __len__(self) -> int:
        """Retourne le nombre de sommets"""
        return len(self._vertices)

    def convex(self) -> bool:
        """Retourne True si le polygon est convexe.
        Actuellement pas implémenté."""
        return self._convex

    def updateAngleCosSin(self) -> None:
        """Met angleCosSin() à jour, appelée automatiquement."""
        self._angleCosSin = [fun(self.angle()) for fun in [cos, sin]]

    def angleCosSin(self, deltaTime: float = 0) -> List[float]:
        """Retourne les valeurs de respectivement cos et sin de l'angle de l'objet au temps donné."""
        if not deltaTime:
            return self._angleCosSin
        angle = super().angle(deltaTime=deltaTime)
        if math.isclose(angle, self._angle, abs_tol=Polygon.precision):
            return self._angleCosSin
        elif math.isclose(angle, self._angleCosSin2Angle, abs_tol=Polygon.precision):
            return self._angleCosSin2
        else:
            self._angleCosSin2 = [fun(angle) for fun in [cos, sin]]
            self._angleCosSin2Angle = angle
            return self._angleCosSin2

    def set_angle(self, newAngle: float) -> None:
        super().set_angle(newAngle)
        self.updateAngleCosSin()

    def rotate(self, angle: float) -> None:
        super().rotate(angle)
        self.updateAngleCosSin()

    def vertex(self, vertexIndex: int, deltaTime: float = 0) -> lib.Point:
        """Retourne le sommet correspondant, tient compte de l'angle et du centre de l'objet."""
        vertexV = lib.Vector(self._vertices[vertexIndex])
        vertexV.rotateCosSin(*self.angleCosSin(deltaTime))
        vertex = lib.Point(vertexV)
        vertex.translate(lib.Vector(self.center(deltaTime)))
        return vertex

    def vertices(self, deltaTime: float = 0) -> List[lib.Point]:
        """Retourne la liste des sommets, tient compte de l'angle et du centre de l'objet."""
        return [self.vertex(i, deltaTime) for i in range(len(self))]

    def edge(self, startVertexIndex: int, deltaTime: float = 0) -> lib.Segment:
        """NE PAS MODIFIER
        Retourne le côté reliant le sommet correspondant et le suivant, tient compte de l'angle et du centre de l'objet."""
        endVertexIndex = startVertexIndex + 1
        if endVertexIndex == len(self):
            endVertexIndex = 0
        return lib.Segment(
            self.vertex(startVertexIndex, deltaTime),
            self.vertex(endVertexIndex, deltaTime),
        )

    def edges(self, deltaTime: float = 0) -> List[lib.Segment]:
        """NE PAS MODIFER
        Retourne la liste des côtés, tient compte de l'angle et du centre de l'objet."""
        edges = []
        vertices = self.vertices(deltaTime)
        second = len(vertices) - 1
        for first in range(len(vertices)):
            edges.append(lib.Segment(vertices[first], vertices[second]))
            second = first
        return edges

    def updatePotentialCollisionZone(self, timeInterval: float) -> None:
        def englobingAlignedRetangle(points: List[lib.Point]) -> lib.AlignedRectangle:
            xes = [point.x() for point in points]
            yes = [point.y() for point in points]
            leftBottom = lib.Point((min(xes), min(yes)))
            return lib.AlignedRectangle(
                max(xes) - leftBottom.x(),
                max(yes) - leftBottom.y(),
                leftBottom=leftBottom,
            )

        vertices = self.vertices()
        if self.isStatic():
            self._potentialCollisionZone = englobingAlignedRetangle(vertices)
        else:
            self._potentialCollisionZone = englobingAlignedRetangle(
                vertices + self.vertices(timeInterval)
            )
        return super().updatePotentialCollisionZone(timeInterval)

    def collides(self, other: "Object", timeInterval: float) -> bool:
        if not super().collides(other, timeInterval):
            return False

        elif isinstance(other, Circle):
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
                projection: lib.Point = edge.orthogonalProjection(other.center())
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
                    lib.Vector.fromPoints(other.center(), nearestVertex).normalVector(),
                )

        elif isinstance(other, Polygon):

            def findNearest(
                edges: List[lib.Segment], vertices: List[lib.Point]
            ) -> Tuple[float, lib.Point, lib.Vector]:
                smallestSquareDistance = math.inf
                for edge in edges:
                    for vertex in vertices:
                        projection: lib.Point = edge.orthogonalProjection(vertex)
                        if edge.passBy(projection):
                            squareDistance = vertex.squareDistanceOf(projection)
                            if squareDistance < smallestSquareDistance:
                                smallestSquareDistance = squareDistance
                                nearestVertex = vertex
                                nearestEdge = edge
                return smallestSquareDistance, nearestVertex, nearestEdge.vector()

            try:
                nearest1 = findNearest(self.edges(), other.vertices())
            except UnboundLocalError:
                nearest2 = findNearest(other.edges(), self.vertices())
                return nearest2[1], nearest2[2]

            try:
                nearest2 = findNearest(other.edges(), self.vertices())
            except UnboundLocalError:
                return nearest1[1], nearest1[2]

            nearests = (nearest1, nearest2)
            nearest = 0
            if nearests[1][0] < nearests[0][0]:
                nearest = 1
            return nearests[nearest][1], nearests[nearest][2]

        else:
            return other.collisionPointAndTangent(self)

    def verticesBeforeRotation(self):
        listOfVerticesBeforeRotation = []
        for vertex in self._vertices:
            vertexPoint = lib.Point(vertex)
            vertexPoint.translate(lib.Vector(self.center()))
            listOfVerticesBeforeRotation.append((vertexPoint[0], vertexPoint[1]))

        return listOfVerticesBeforeRotation

    def toMinimalDict(self) -> dict:
        dic = super().toMinimalDict()
        dic.update({"vertices": [tuple(v) for v in self._vertices]})
        return dic
