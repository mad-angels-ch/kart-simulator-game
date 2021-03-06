import math
from typing import Tuple

import lib
from lib.Point import Point, Vector

from .Object import Object


class Circle(Object):
    """Classe des cercles."""

    _radius: float

    def __init__(self, **kwargs) -> None:
        super().__init__(**kwargs)
        self._radius = kwargs.get("radius", 1)

    def radius(self) -> float:
        """Retourne le rayon du cercle."""
        return self._radius

    def updatePotentialCollisionZone(self, timeInterval: float) -> None:
        if self.isStatic():
            self._potentialCollisionZone = lib.AlignedRectangle(
                self.radius() * 2, self.radius() * 2, center=self.center()
            )
        else:
            translation = self.relativePosition(timeInterval)
            self._potentialCollisionZone = lib.AlignedRectangle(
                self.radius() * 2 + translation.x(),
                self.radius() * 2 + translation.y(),
                center=lib.Point(lib.Vector(self.center()) + translation / 2),
            )
        return super().updatePotentialCollisionZone(timeInterval)

    def collides(self, other: "Object", timeInterval: float) -> bool:
        if not super().collides(other, timeInterval):
            return False

        elif isinstance(other, Circle):
            newSelf = lib.Circle(self.center(timeInterval), self.radius())
            newOther = lib.Circle(other.center(timeInterval), other.radius())
            if newSelf.collides(newOther):
                return True

            # contrôller que les cercles ne se sont pas passés par dessus
            selfTrajectory = None
            if self.center().distanceOf(newSelf.center()) > self.radius():
                normalTrajectoryVector = lib.Vector.fromPoints(
                    self.center(), newSelf.center()
                ).normalVector()
                normalTrajectoryVector.set_norm(self.radius())
                v0 = lib.Point(self.center())
                v1 = lib.Point(self.center())
                v2 = lib.Point(newSelf.center())
                v0.translate(-normalTrajectoryVector)
                v1.translate(normalTrajectoryVector)
                v2.translate(normalTrajectoryVector)
                selfTrajectory = lib.Rectangle(v0, v1, v2)
                if selfTrajectory.collides(newOther):
                    return True

            otherTrajectory = None
            if other.center().distanceOf(newOther.center()) > other.radius():
                normalTrajectoryVector = lib.Vector.fromPoints(
                    other.center(), newOther.center()
                ).normalVector()
                normalTrajectoryVector.set_norm(other.radius())
                v0 = lib.Point(other.center())
                v1 = lib.Point(other.center())
                v2 = lib.Point(newOther.center())
                v0.translate(-normalTrajectoryVector)
                v1.translate(normalTrajectoryVector)
                v2.translate(normalTrajectoryVector)
                otherTrajectory = lib.Rectangle(v0, v1, v2)
                if otherTrajectory.collides(newSelf):
                    True

            if selfTrajectory and otherTrajectory:
                return selfTrajectory.collides(otherTrajectory)

            else:
                return False

        else:
            return other.collides(self, timeInterval)

    def collisionPointAndTangent(self, other: "Object") -> Tuple[lib.Point, lib.Vector]:
        if isinstance(other, Circle):
            translation = lib.Vector.fromPoints(self.center(), other.center())
            translation.set_norm(self.radius())
            collisionPoint = lib.Point(self.center())
            collisionPoint.translate(translation)
            return (
                collisionPoint,
                lib.Vector.fromPoints(self.center(), other.center()).normalVector(),
            )

        else:
            return other.collisionPointAndTangent(self)

    def toMinimalDict(self) -> dict:
        dic = super().toMinimalDict()
        dic.update({"radius": self._radius})
        return dic
