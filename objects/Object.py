from typing import Tuple

import lib

from . import motions
from .fill import Fill, Hex, Pattern


class Object:
    """Classes des objets composants les différents mondes.
    Ne pas utiliser directement, utiliser les classes filles."""

    precision = 1e-6
    fillClasses = {fill.__name__: fill for fill in [Hex, Pattern]}
    timeToKeepLastCollided = 1 / 60

    _formID: int
    _name: str

    _angle: float
    _center: lib.Point
    _angularMotion: motions.angulars.AngularMotion
    _vectorialMotion: motions.vectorials.VectorialMotion

    _fill: Fill
    _opacity: float
    _mass: float
    _friction: float

    _potentialCollisionZone: lib.AlignedRectangle
    _potentialCollisionZoneUpToDate: bool = False
    _potentialCollisionZoneTimeInterval: float

    _solid: bool
    _destroy: bool = False

    _lastCollided: "Object" = None
    _elapsedTimeLastCollision: float = 0

    def fromMinimalDict(obj: dict) -> dict:
        """Retourne les argument pour reproduire l'objet représenté par le dict python du même format qu'exporté par toMinimalDict()"""
        obj["fill"] = Object.fillClasses[obj["fill"]["class"]].fromDict(obj["fill"])
        obj["center"] = lib.Point(obj["center"])
        return obj

    def __init__(self, **kwargs) -> None:
        self._formID = kwargs["formID"]
        self._angle = kwargs.get("angle", 0)
        self._name = kwargs.get("name", "")

        self._center = kwargs.get("center", lib.Point())
        self._angularMotion = kwargs.get(
            "angularMotion", motions.angulars.AngularMotion()
        )
        self._vectorialMotion = kwargs.get(
            "vectorialMotion", motions.vectorials.VectorialMotion()
        )
        self._fill = kwargs.get("fill", Hex("#000000"))
        self._opacity = kwargs.get("opacity", 1)
        self._mass = kwargs.get("mass", 0)
        self._friction = kwargs.get("friction", 0)
        self._solid = kwargs.get("isSolid", True)

    def __eq__(self, other: "Object") -> bool:
        """Retourne vrai s'il s'agit du même objet"""
        return other != None and self.formID() == other.formID()

    def onEventsRegistered(self, deltaTime: float) -> None:
        """Méthode à surcharger, lancée une fois les évènements traités"""

    def onCollision(self, other: "Object") -> None:
        """Méthode lancé lors des collisions"""
        self._lastCollided = other
        self._elapsedTimeLastCollision = 0

    def isSolid(self) -> bool:
        """Si vrai, l'objet rebondit sur les autres objets sinon il les traverse"""
        return self._solid

    def name(self) -> str:
        """Retourne le nom de l'objet.
        Plusieurs objets peuvent avoir le même nom"""
        return self._name

    def formID(self) -> int:
        """Retourne un identifiant unique pour l'objet. Ne changera jamais."""
        return self._formID

    def angle(self, deltaTime: float = 0) -> float:
        """Retourne la rotation de l'objet par rapport à son centre à l'instant donné."""
        if not deltaTime:
            return self._angle
        return self._angle + self.relativeAngle(deltaTime)

    def center(self, deltaTime: float = 0) -> lib.Point:
        """NE PAS MODIFIER\n
        Retourne le centre de l'objet à l'instant donné."""
        if not deltaTime:
            return self._center

        newCenter = lib.Point(self.center())
        newCenter.translate(self.relativePosition(deltaTime))
        return newCenter

    def rotationCenter(self, deltaTime: float = 0) -> lib.Point:
        """Retourne le centre de rotation de l'objet à l'instant donné."""
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
        """Retourne vrai si l'objet est imobile"""
        return self._angularMotion.isStatic() and self._vectorialMotion.isStatic()

    def relativeAngle(self, timeInterval: float) -> float:
        """Retourne la rotation de l'objet durant l'intervalle donné."""
        return self._angularMotion.relativeAngle(timeInterval)

    def relativePosition(self, timeInterval: float) -> lib.Vector:
        """Retourne la transtion de l'objet durant l'intervalle donné."""
        fromRotationCenterBefore = lib.Vector.fromPoints(
            self.rotationCenter(), self.center()
        )
        fromRotationCenterAfter = lib.Vector(fromRotationCenterBefore)
        fromRotationCenterAfter.rotate(self.relativeAngle(timeInterval))
        return (
            self._vectorialMotion.relativePosition(timeInterval)
            - fromRotationCenterBefore
            + fromRotationCenterAfter
        )

    def speed(self, deltaTime: float = 0) -> lib.Vector:
        """Retourne la vitesse de translation du centre de l'objet"""
        return self.speedAtPoint(self.center(deltaTime), deltaTime)

    def speedAtPoint(self, point: lib.Point, deltaTime: float = 0) -> lib.Vector:
        """Retourne la vitesse linéaire d'un point donné (tient compte de sa vitesse angulaire)"""
        normal = lib.Vector.fromPoints(self.rotationCenter(), point)
        rtanSpeed = lib.Vector((0, self.angularMotionSpeed(deltaTime) * normal.norm()))
        rtanSpeed.rotate(normal.direction())
        return rtanSpeed + self.vectorialMotionSpeed(deltaTime)

    def accelerationAtPoint(self, point: lib.Point, deltaTime: float = 0) -> lib.Vector:
        """Retourne l'accélération linéaire d'un point donné (tient compte de son accélération angulaire)"""
        normal = lib.Vector.fromPoints(self.rotationCenter(), point)
        rTanAcceleration = lib.Vector(
            (0, self.angularMotionAcceleration(deltaTime) * normal.norm())
        )
        rTanAcceleration.rotate(normal.direction())
        return rTanAcceleration + self.vectorialMotionAcceleration(deltaTime)

    def set_angle(self, newAngle: float) -> None:
        """Change l'angle de l'objet au temps 0"""
        self._angle = newAngle
        self._potentialCollisionZoneUpToDate = False

    def set_center(self, newCenter: lib.Point) -> None:
        """Change le centre de l'objet au temps 0"""
        self._center = newCenter
        self._potentialCollisionZoneUpToDate = False

    def rotate(self, angle: float) -> None:
        """Effectue une rotation sur l'objet"""
        self._angle += angle
        self._potentialCollisionZoneUpToDate = False

    def translate(self, vector: lib.Vector) -> None:
        """Effectue une translation sur l'objet"""
        self._center.translate(vector)
        self._potentialCollisionZoneUpToDate = False

    def updateReferences(self, deltaTime: float) -> None:
        """Avance les références: avance l'instant correspondant au temps 0 de deltaTime"""
        self.rotate(self.relativeAngle(deltaTime))
        self.translate(self.relativePosition(deltaTime))

        self._angularMotion.updateReferences(deltaTime)
        self._vectorialMotion.updateReferences(deltaTime)

        if self._lastCollided:
            self._elapsedTimeLastCollision -= deltaTime
            if self._elapsedTimeLastCollision > self.timeToKeepLastCollided:
                self._lastCollided = None

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
        """Retourne la méthode de remplissage de l'objet."""
        return self._fill

    def set_fill(self, newFill: Fill) -> None:
        """Change la méthode de remplissage de l'objet."""
        self._fill = newFill

    def opacity(self) -> float:
        """Retourne la transparance de l'objet."""
        return self._opacity

    def mass(self) -> float:
        """Retourne la masse de l'objet.
        Une mass de 0 signifie que ses mouvements ne seront pas influencés par les autres objets."""
        return self._mass

    def set_mass(self, newMass: float) -> None:
        """Change la masse de l'objet.
        Une mass de 0 signifie que ses mouvements ne seront pas influencés par les autres objets."""
        self._mass = newMass

    def friction(self) -> float:
        """Retourne le coeffiction de frottement de l'objet.\n
        Un coefficient de 0 signifie que l'objet n'a aucune perte lors des collisons.
        Un coefficient de 1 signifie que l'objet est complétement imobile après une collisions. Ne pas utiliser.
        Un coefficient négatif signifie que l'objet prend de la vitesse lors des collisions."""
        return self._friction

    def set_friction(self, newFriction: float) -> None:
        """Change le coefficient de friction de l'objet.\n
        Un coefficient de 0 signifie que l'objet n'a aucune perte lors des collisons.
        Un coefficient de 1 signifie que l'objet est complétement imobile après une collisions. Ne pas utiliser.
        Un coefficient négatif signifie que l'objet prend de la vitesse lors des collisions."""
        self._friction = newFriction

    def lastCollided(self, deltaTime: float = 0) -> "Object | None":
        """Retourne le dernier objet avec lequel celui-ci est entré en collision, s'il existe."""
        if self._elapsedTimeLastCollision + deltaTime > self.timeToKeepLastCollided:
            return self._lastCollided

    def collides(self, other: "Object", timeInterval: float) -> bool:
        """Retourne vrai si les deux objets se collisionnent dans l'intervalle de temps donné
        Les collisions entres deux objets fixés sont ignorés (ceux qui ont une masse nulle)"""
        return (self.mass() > 0 or other.mass() > 0) and other != self.lastCollided(
            timeInterval
        )

    def collisionPointAndTangent(self, other: "Object") -> Tuple[lib.Point, lib.Vector]:
        """Retourne une approximation du point par lequel les deux objets se touchent
        ainsi qu'une approximation d'un vecteur directeur de la tangente passant par ce point"""
        assert True, "This method should be overwritten"

    def groupID(self) -> int:
        """Return the id of this object's group"""
        from .ObjectFactory import ObjectFactory

        return self.formID() // ObjectFactory.maxObjectsPerGroup

    def destroy(self) -> None:
        """Demande à être supprimé à la fin de la frame"""
        self._destroy = True

    def restore(self) -> None:
        """Demande à ne pas être supprimé à la fin de la frame"""
        self._destroy = False

    def lastFrame(self) -> bool:
        """Retourne vrai si l'objet n'existera plus à la prochaine frame"""
        return self._destroy

    def toMinimalDict(self) -> dict:
        """Exporte cet objet dans un dict python contant toutes les informations pour reproduire visuellement l'objet"""
        return {
            "class": self.__class__.__name__,
            "formID": self._formID,
            "angle": self._angle,
            "center": tuple(self._center),
            "fill": self._fill.toDict(),
            "opacity": self._opacity,
        }
