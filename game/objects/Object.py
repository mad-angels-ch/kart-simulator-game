from typing import Tuple
import math

import lib

from . import motions


class Object:
    precision = 1e-6

    _name: str
    _formID: int

    _angle: float
    _center: lib.Point
    _angularMotion: motions.angulars.AngularMotion
    _vectorialMotion: motions.vectorials.VectorialMotion

    _fill: str
    _opacity: float
    _mass: float
    _friction: float

    _potentialCollisionZone: lib.AlignedRectangle
    _potentialCollisionZoneUpToDate: bool
    _potentialCollisionZoneTimeInterval: float

    def __init__(self, **kwargs) -> None:
        self._name = kwargs.get("name", None)
        self._formID = kwargs["formID"]
        self._angle = kwargs.get("angle", 0)
        self._center = kwargs.get("center", lib.Point())
        self._angularMotion = kwargs.get(
            "angularMotion", motions.angulars.AngularMotion()
        )
        self._vectorialMotion = kwargs.get(
            "vectorialMotion", motions.vectorials.VectorialMotion()
        )
        self._fill = kwargs.get("fill", "")
        self._opacity = kwargs.get("opacity", 1)
        self._mass = kwargs.get("mass", 0)
        self._friction = kwargs.get("friction", 0)
        self._potentialCollisionZoneUpToDate = False

    def formID(self) -> int:
        return self._formID

    def name(self) -> str:
        return self._name

    def angle(self, deltaTime: float = 0) -> float:
        if not deltaTime:
            return self._angle
        return self._angle + self.relativeAngle(deltaTime)

    def center(self, deltaTime: float = 0) -> lib.Point:
        if not deltaTime:
            return self._center

        newCenter = lib.Point(self.center())
        newCenter.translate(self.relativePosition(deltaTime))
        return newCenter

    def potentialCollisionZone(self, timeInterval: float) -> lib.AlignedRectangle:
        """Retourne un rectangle aligné avec les axes englobant toutes les positions de l'objet pendant l'intervalle donné."""
        if (
            not self._potentialCollisionZoneUpToDate
            or self._potentialCollisionZoneTimeInterval != timeInterval
        ):
            self.updatePotentialCollisionZone(timeInterval=timeInterval)

        return self._potentialCollisionZone

    def updatePotentialCollisionZone(self, timeInterval: float) -> None:
        """Met le rectangle aligné avec les axes englobant toutes les positions de l'objet à jour pour l'intervalle donné.
        À surcharger"""
        self._potentialCollisionZoneTimeInterval = timeInterval
        self._potentialCollisionZoneUpToDate = True

    def isStatic(self) -> bool:
        return self._angularMotion.isStatic() and self._vectorialMotion.isStatic()

    def relativeAngle(self, deltaTime: float) -> float:
        return self._angularMotion.relativeAngle(deltaTime)

    def relativePosition(self, deltaTime: float) -> lib.Vector:
        fromRotationCenterBefore = lib.Vector.fromPoints(
            self._angularMotion.center(), self.center()
        )
        fromRotationCenterAfter = lib.Vector(fromRotationCenterBefore)
        fromRotationCenterAfter.rotate(self.relativeAngle(deltaTime))
        return (
            self._vectorialMotion.relativePosition(deltaTime)
            - fromRotationCenterBefore
            + fromRotationCenterAfter
        )

    def speedAtPoint(self, point: lib.Point, deltaTime: float = 0) -> lib.Vector:
        return self._angularMotion.speedAtPoint(
            point, deltaTime
        ) + self._vectorialMotion.speed(deltaTime)

    def centerSpeed(self, deltaTime: float = 0) -> lib.Vector:
        return self.speedAtPoint(self.center(deltaTime), deltaTime)

    def set_angle(self, newAngle: float) -> None:
        self._angle = newAngle
        self._potentialCollisionZoneUpToDate = False

    def set_center(self, newCenter: lib.Point) -> None:
        self._center = newCenter
        self._potentialCollisionZoneUpToDate = False

    def rotate(self, angle: float) -> None:
        self._angle += angle
        self._potentialCollisionZoneUpToDate = False

    def translate(self, vector: lib.Vector) -> None:
        self._center.translate(vector)
        self._potentialCollisionZoneUpToDate = False

    def updateReferences(self, deltaTime: float) -> None:
        self.rotate(self.relativeAngle(deltaTime))
        self.translate(self.relativePosition(deltaTime))

        self._angularMotion.updateReferences(deltaTime)
        self._angularMotion.center().translate(
            self._vectorialMotion.relativePosition(deltaTime)
        )
        self._vectorialMotion.updateReferences(deltaTime)

    def angularMotionSpeed(self, deltaTime: float = 0) -> float:
        """Attention, utilisation avancée uniquement
        Retourne la vitesse angulaire de l'objet."""
        return self._angularMotion.speed(deltaTime=deltaTime)

    def set_angularMotionSpeed(self, newSpeed: float) -> None:
        """Attention, utilisation avancée uniquement
        Modifie la vitesse angulaire de l'objet."""
        self._angularMotion.set_speed(newSpeed=newSpeed)
        self._potentialCollisionZoneUpToDate = False

    def angularMotionAcceleration(self, deltaTime: float = 0) -> float:
        """Attention, utilisation avancée uniquement
        Retourne l'accélération angulaire de l'objet."""
        return self._angularMotion.acceleration(deltaTime=deltaTime)

    def set_angularMotionAcceleration(self, newAcceleration: float) -> None:
        """Attention, utilisation avancée uniquement
        Modifie la vitesse angulaire de l'objet."""
        self._angularMotion.set_acceleration(newAcceleration=newAcceleration)
        self._potentialCollisionZoneUpToDate = False

    def vectorialMotionSpeed(self, deltaTime: float = 0) -> lib.Vector:
        """NE PAS MODIFIER, utiliser set_vectorialMotionSpeed()
        Attention, utilisation avancée uniquement
        Retourne la vitesse vectoriel de l'objet, sans tenir compte de sa rotation.
        """
        return self._vectorialMotion.speed(deltaTime=deltaTime)

    def set_vectorialMotionSpeed(self, newSpeed: lib.Vector) -> None:
        """Attention, utilisation avancée uniquement
        Modifie la vitesse vectoriel de l'objet, sans tenir compte de sa rotation"""
        self._vectorialMotion.set_speed(newSpeed=newSpeed)
        self._potentialCollisionZoneUpToDate = False

    def vectorialMotionAcceleration(self, deltaTime: float = 0) -> lib.Vector:
        """NE PAS MODIFIER, utiliser set_vectorialMotionAcceleration()
        Attention, utilisation avancée uniquement
        Retourne l'accélération vectoriel de l'objet, sans tenir compte de sa rotation.
        """
        self._vectorialMotion.acceleration(deltaTime=deltaTime)

    def set_vectorialMotionAcceleration(self, newAcceleration: lib.Vector) -> None:
        """Attention, utilisation avancée uniquement
        Modifie l'accélération vectoriel de l'objet, sans tenir compte de sa rotation"""
        self._vectorialMotion.set_acceleration(newAcceleration=newAcceleration)
        self._potentialCollisionZoneUpToDate = False

    def fill(self) -> str:
        return self._fill

    def set_fill(self, color: str) -> None:
        self._fill = color

    def opacity(self) -> float:
        return self._opacity

    def mass(self) -> float:
        return self._mass

    def friction(self) -> float:
        return self._friction

    def collides(self, other: "Object", timeInterval: float) -> bool:
        """Retourne vrai si les deux objets se collisionnent dans l'intervalle de temps donné
        Les collisions entres deux objets fixés sont ignorés (ceux qui ont une masse nulle)"""
        raise RuntimeError("This method should be overwritten")

    def collisionPointAndTangent(self, other: "Object") -> Tuple[lib.Point, lib.Vector]:
        """Retourne une approximation du point par lequel les deux objets se touchent
        ainsi qu'une approximation d'un vecteur directeur de la tangente passant par ce point"""
        raise RuntimeError("This method should be overwritten")

    # def xyz(self, other: "Object", deltaTime: float = 0) -> bool:
    #     point, tangent = self.collisionPointAndTangent(other)
    #     selfNetForce = self.netForceAtPoint()
    #     if selfNetForce:

    # def netForceAtPoint(self, point: lib.Point, deltaTime: float = 0) -> lib.Vector:
    #     return self.mass() * (
    #         self._angularMotion.accelerationAtPoint(point, deltaTime)
    #         + self._vectorialMotion.acceleration(deltaTime)
    #     )

    def vectorialMotion(self):
        return self._vectorialMotion