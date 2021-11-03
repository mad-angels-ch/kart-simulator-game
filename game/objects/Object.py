from typing import Tuple
import lib

from . import motions


class Object:
    _name: str
    _formID: int

    _center: lib.Point
    _angle: float
    angularMotion: motions.angulars.AngularMotion
    vectorialMotion: motions.vectorials.VectorialMotion

    _fill: str
    _opacity: float
    _mass: float
    _friction: float

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

        newCenter = lib.Point(*self.center())
        newCenter.translate(self.relativePosition(deltaTime))
        return newCenter

    def relativeAngle(self, deltaTime: float) -> float:
        return self.angularMotion.relativeAngle(deltaTime)

    def relativePosition(self, deltaTime: float) -> lib.Vector:
        fromRotationCenterBefore = lib.Vector.fromPoints(
            self.angularMotion.center(), self.center()
        )
        fromRotationCenterAfter = lib.Vector(*fromRotationCenterBefore)
        fromRotationCenterAfter.rotate(self.angularMotion.relativeAngle(deltaTime))
        return (
            self.vectorialMotion.relativePosition(deltaTime)
            - fromRotationCenterBefore
            + fromRotationCenterAfter
        )

    def speedAtPoint(self, point: lib.Point, deltaTime: float = 0) -> lib.Vector:
        return self.angularMotion.speedAtPoint(
            point, deltaTime
        ) + self.vectorialMotion.speed(deltaTime)

    def centerSpeed(self, deltaTime: float = 0) -> lib.Vector:
        return self.speedAtPoint(self.center(deltaTime), deltaTime)

    def set_angle(self, newAngle: float) -> None:
        self._angle = newAngle

    def set_center(self, newCenter: lib.Point) -> None:
        self._center = newCenter

    def rotate(self, angle: float) -> None:
        self._angle += angle

    def translate(self, vector: lib.Vector) -> None:
        self._center.translate(vector)

    def updateReferences(self, deltaTime: float) -> None:
        # mise à jour de la vitesse angulaire
        # self.set_angle(self.angle(deltaTime))
        self.rotate(self.relativeAngle(deltaTime))
        self.angularMotion.updateReferences(deltaTime)
        rotationCenter = lib.Point(*self.angularMotion.center())
        rotationCenter.translate(self.vectorialMotion.relativePosition(deltaTime))
        self.angularMotion.set_center(rotationCenter)

        # mise à jour de la vitesse vectorielle
        self.translate(self.relativePosition(deltaTime))
        self.vectorialMotion.updateReferences(deltaTime)

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
        return False

    def collisionPointAndTangent(self, other: "Object") -> Tuple[lib.Point, lib.Vector]:
        """Retourne une approximation du point par lequel les deux objets se touchent
        ainsi qu'une approximation d'un vecteur directeur de la tangente passant par ce point"""
        return other.center(), lib.Vector(0, 0)
