from typing import Tuple
import math

import lib

from . import motions
from .fill import Fill, createFill


class Object:
    precision = 1e-6

    _name: str
    _formID: int

    _angle: float
    _center: lib.Point
    _angularMotion: motions.angulars.AngularMotion
    _vectorialMotion: motions.vectorials.VectorialMotion

    _fill: Fill
    _opacity: float
    _mass: float
    _friction: float

    _potentialCollisionZone: lib.AlignedRectangle
    _potentialCollisionZoneUpToDate: bool
    _potentialCollisionZoneTimeInterval: float

    _solid: bool

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
        self._fill = kwargs.get("fill", createFill(type="Hex", hexColor="#000000"))
        self._opacity = kwargs.get("opacity", 1)
        self._mass = kwargs.get("mass", 0)
        self._friction = kwargs.get("friction", 0)
        self._potentialCollisionZoneUpToDate = False
        self._solid = kwargs.get("isSolid", True)
        self._solid = kwargs.get("isSolid", True)

    def __eq__(self, other: "Object") -> bool:
        return self.formID() == other.formID()

    def onFrameStart(self, deltaTime: float) -> None:
        """Méthode destinée à être surchargée, lancée au début de chaque frame"""
        pass

    def onEventsRegistered(self, deltaTime: float) -> None:
        """Méthode à surcharger"""
        pass

    def onCollision(self, other: "Object", timeSinceLastFrame: float) -> None:
        """Méthode à surcharger, lancée lors des collisions"""

    def onFrameEnd(self, deltaTime: float) -> None:
        """Méthode destinée à être surchargée, lancée à la fin de chaque frame"""
        pass

    def isSolid(self) -> bool:
        """Si vrai, il rebondit sur les autres objets sinon il les traverse"""
        return self._solid

    def formID(self) -> int:
        return self._formID

    def name(self) -> str:
        return self._name

    def angle(self, deltaTime: float = 0) -> float:
        if not deltaTime:
            return self._angle
        return self._angle + self.relativeAngle(deltaTime)

    def center(self, deltaTime: float = 0) -> lib.Point:
        """NE PAS MODIFIER
        Retourne le centre de l'objet."""
        if not deltaTime:
            return self._center

        newCenter = lib.Point(self.center())
        newCenter.translate(self.relativePosition(deltaTime))
        return newCenter

    def rotationCenter(self, deltaTime: float = 0) -> lib.Point:
        """Retourne le centre de rotation de l'objet à l'instant donné"""
        rCenter = lib.Point(self.center(deltaTime))
        rCenter.translate(self._angularMotion.center())
        return rCenter

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
            self.rotationCenter(), self.center()
        )
        fromRotationCenterAfter = lib.Vector(fromRotationCenterBefore)
        fromRotationCenterAfter.rotate(self.relativeAngle(deltaTime))
        return (
            self._vectorialMotion.relativePosition(deltaTime)
            - fromRotationCenterBefore
            + fromRotationCenterAfter
        )

    def speedAtPoint(self, point: lib.Point, deltaTime: float = 0) -> lib.Vector:
        normal = lib.Vector.fromPoints(self.rotationCenter(), point)
        rtanSpeed = lib.Vector((0, self.angularMotionSpeed(deltaTime) * normal.norm()))
        rtanSpeed.rotate(normal.direction())
        return rtanSpeed + self.vectorialMotionSpeed(deltaTime)

    def centerSpeed(self, deltaTime: float = 0) -> lib.Vector:
        return self.speedAtPoint(self.center(deltaTime), deltaTime)

    def accelerationAtPoint(self, point: lib.Point, deltaTime: float = 0) -> lib.Vector:
        normal = lib.Vector.fromPoints(self.rotationCenter(), point)
        rTanAcceleration = lib.Vector(
            (0, self.angularMotionAcceleration(deltaTime) * normal.norm())
        )
        rTanAcceleration.rotate(normal.direction())
        return rTanAcceleration + self.vectorialMotionAcceleration(deltaTime)

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
        return self._vectorialMotion.acceleration(deltaTime=deltaTime)

    def set_vectorialMotionAcceleration(self, newAcceleration: lib.Vector) -> None:
        """Attention, utilisation avancée uniquement
        Modifie l'accélération vectoriel de l'objet, sans tenir compte de sa rotation"""
        self._vectorialMotion.set_acceleration(newAcceleration=newAcceleration)
        self._potentialCollisionZoneUpToDate = False

    def fill(self) -> Fill:
        return self._fill

    def set_fill(self, newFill: Fill) -> None:
        self._fill = newFill

    def opacity(self) -> float:
        return self._opacity

    def mass(self) -> float:
        return self._mass

    def set_mass(self, newMass: float) -> None:
        """Change la masse de l'objet.
        Une mass de 0 signifie qu'il est impossible à influencer."""
        self._mass = newMass

    def friction(self) -> float:
        return self._friction

    def set_friction(self, newFriction: float) -> None:
        """Change le coefficient de friction de l'objet.
        Un coefficient de 0 signifie que l'objet n'a aucune perte lors des collisons.
        Un coefficient de 1 signifie que l'objet est complétement imobile après une collisions. Ne pas utiliser.
        Un coefficient négatif signifie que l'objet prend de la vitesse lors des collisions."""
        self._friction = newFriction

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

    def vectorialMotion(self):
        return self._vectorialMotion
