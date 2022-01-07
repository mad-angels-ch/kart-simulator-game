import math
from typing import List
import lib

from .Polygon import Polygon, Object
from .motions import angulars as angularMotions, vectorials as vectorialMotions


class Kart(Polygon):
    """CREER AVEC LA FACTORY\n
    Classe des karts.
    Ceux-ci peuvent être contrôlés à l'aide des méthodes request_move() et request_turn().
    Le sens du kart est indiqué par le vecteur (1, 0) lorsque l'angle du premier vaut 0.
    Les propriétés <movingSpeed> et <turningSpeed> peuvent être modifiées et représentent les vitesses maximales du kart."""

    # vitesse de déplacement, m/s
    movingSpeed: float = 30
    # vitesse de rotation, rad/s
    turningSpeed: float = 1

    # -1 = en arrière, 0 = arrêté, 1 = en avant
    _moving: int

    # -1 = à droite, 0 = tout droit, 1 = à gauche
    _turning: int

    _remainingTimeToWait: float
    waitAfterCollision: float = 1

    def __init__(self, **kwargs) -> None:
        super().__init__(**kwargs)
        self._angularMotion.set_center(self.center())
        self._vectorialMotion = vectorialMotions.VectorialMotion(
            speed=lib.Vector((10, 0))
        )
        self._moving = 0
        self._turning = 0
        self._remainingTimeToWait = 0

    def request_move(self, direction: int) -> None:
        """Met le kart en mouvement
        -1 = en arrière, 0 = arrêté, 1 = en avant"""
        if direction:
            self._moving = direction

    def request_turn(self, direction: int) -> None:
        """Fait tourner le kart
        -1 = à droite, 0 = tout droit, 1 = à gauche"""
        self._turning = direction

    # def set_center(self, newCenter: lib.Point) -> None:
    #     super().set_center(newCenter)

    # def translate(self, vector: lib.Vector) -> None:
    #     super().translate(vector)

    # def set_angle(self, newAngle: float) -> None:
    #     super().set_angle(newAngle)

    # def rotate(self, angle: float) -> None:
    #     super().rotate(angle)

    # def set_angularMotionSpeed(self, newSpeed: float) -> None:
    #     super().set_angularMotionSpeed(newSpeed)

    # def set_vectorialMotionSpeed(self, newSpeed: lib.Vector) -> None:
    #     super().set_vectorialMotionSpeed(newSpeed)

    def onCollision(self, other: "Object") -> None:
        # self._remainingTimeToWait = self.waitAfterCollision
        pass

    def onEventsRegistered(self, deltaTime: float) -> None:
        # if not self._remainingTimeToWait:
        if self._turning:
            self.set_angularMotionSpeed(self._turning * self.turningSpeed)
        if self._moving:
            targetSpeed = lib.Vector((self._moving * self.movingSpeed, 0))
            targetSpeed.rotate(self.angle())
            self.set_vectorialMotionSpeed(targetSpeed)

    # def updateReferences(self, deltaTime: float) -> None:
    #     super().updateReferences(deltaTime)
    # if self._remainingTimeToWait:
    #     if self._remainingTimeToWait > deltaTime:
    #         self._remainingTimeToWait -= deltaTime
    #     else:
    #         self._remainingTimeToWait = 0
