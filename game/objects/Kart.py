from logging import currentframe
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
    Les propriétés <movingSpeed> (m/s), <movingCorrectionTime>(s), <turningSpeed>(rad/s) et <turningCorrectionTime> (s)
    peuvent être modifiées et représentent les vitesses maximales et temps de correction du kart."""

    movingSpeed: float = 500
    movingCorrectionTime: float = 0.5
    turningSpeed: float = 4
    turningCorrectionTime: float = 0.2

    # -1 = en arrière, 0 = arrêté, 1 = en avant
    _moving: int

    # -1 = à droite, 0 = tout droit, 1 = à gauche
    _turning: int

    def __init__(self, **kwargs) -> None:
        kwargs["mass"] = 1
        kwargs["friction"] = 0.01
        super().__init__(**kwargs)
        rCenter = lib.Point(self.vertex(-1))
        rCenter.translate(lib.Vector.fromPoints(self.vertex(-1), self.vertex(-2)) / 2)
        self._angularMotion = angularMotions.UniformlyAcceleratedCircularMotion(
            rotationCenter=rCenter
        )
        self._vectorialMotion = vectorialMotions.UniformlyAcceleratedMotion()
        self._moving = 0
        self._turning = 0

    def request_move(self, direction: int) -> None:
        """Met le kart en mouvement
        -1 = en arrière, 0 = arrêté, 1 = en avant"""
        self._moving = direction

    def request_turn(self, direction: int) -> None:
        """Fait tourner le kart
        -1 = à droite, 0 = tout droit, 1 = à gauche"""
        self._turning = direction

    def onCollision(self, other: "Object", timeSinceLastFrame: float) -> None:
        self.set_angularMotionSpeed(0)
        self.set_angularMotionAcceleration(0)

    def onEventsRegistered(self, deltaTime: float) -> None:
        targetASpeed = self._turning * self.turningSpeed
        currentASpeed = self.angularMotionSpeed()
        self.set_angularMotionAcceleration(
            (targetASpeed - currentASpeed) / self.turningCorrectionTime
        )

        targetVectorialSpeed = lib.Vector((self._moving * self.movingSpeed, 0))
        targetVectorialSpeed.rotate(self.angle())
        currentVectorialSpeed = self.vectorialMotionSpeed()
        acceleration = lib.Vector()
        for i in range(2):
            acceleration[i] = (
                targetVectorialSpeed[i] - currentVectorialSpeed[i]
            ) / self.movingCorrectionTime
        self.set_vectorialMotionAcceleration(acceleration)
