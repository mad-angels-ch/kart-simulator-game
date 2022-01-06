import math
from typing import List
import lib

from .Polygon import Polygon
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

    def __init__(self, **kwargs) -> None:
        super().__init__(**kwargs)
        self._vectorialMotion = vectorialMotions.VectorialMotion()
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

    def set_center(self, newCenter: lib.Point) -> None:
        super().set_center(newCenter)

    def translate(self, vector: lib.Vector) -> None:
        super().translate(vector)

    def set_angle(self, newAngle: float) -> None:
        super().set_angle(newAngle)

    def rotate(self, angle: float) -> None:
        super().rotate(angle)

    def set_angularMotionSpeed(self, newSpeed: float) -> None:
        super().set_angularMotionSpeed(newSpeed)

    def set_vectorialMotionSpeed(self, newSpeed: lib.Vector) -> None:
        super().set_vectorialMotionSpeed(newSpeed)

    def updateReferences(self, deltaTime: float) -> None:
        acceleration = lib.Vector((self.movingSpeed * self._moving, 0))
        acceleration.rotate(self.angle())
        self.set_vectorialMotionSpeed(acceleration)
        super().updateReferences(deltaTime)
