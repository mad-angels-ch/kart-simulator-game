from typing import List
from logging import info, warning
from math import sin, cos

from lib import Point, Vector, Segment

from .Object import Object
from .Circle import Circle


class Polygon(Object):
    _summits: List[Point]
    _angleCosSin: List[float]

    def __init__(self) -> None:
        super().__init__()
        self._summits = list()
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

    def rel_summits(self) -> List[Point]:
        """Retourne la coordonnée relative des sommets,
        par rapport au centre et à l'angle"""
        return self._summits

    def rel_summit(self, summitIndex: int) -> Point:
        """Retourne la coordonnée relative du sommet,
        par rapport au centre et à l'angle"""
        return self._summits[summitIndex]

    def abs_summit(self, deltaTime: float = 0) -> Point:
        """Retourne la coordonnée absolue des sommets,
        en tenant compte du centre et de l'angle"""
        return [self.abs_summit(i, deltaTime) for i in range(len(self.rel_summits()))]

    def abs_summit(self, summitIndex: int, deltaTime: float = 0) -> Point:
        """Retourne la coordonnée absolue du sommet,
        en tenant compte du centre et de l'angle"""
        summitV = Vector(*self.rel_summit(summitIndex))
        summitV.rotateCosSin(self.angleCosSin(deltaTime))
        summitP = Point(*summitV)
        summitP.translate(Vector(*self.center(deltaTime)))
        return summitP

    def collides(self, object: "Object") -> bool:
        if isinstance(object, Circle):
            second = len(self.rel_summits())
            for first in range(len(self.rel_summits())):
                summit = self.abs_summit(first)

                # collision sur un sommet
                if summit.distanceOf(object.center()) < object.radius():
                    return True

                # collision sur un côté
                side = Segment(summit, self.abs_summit(second))
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
