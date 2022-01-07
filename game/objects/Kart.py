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
    Les propriétés <movingSpeed> et <turningSpeed> peuvent être modifiées et représentent les vitesses maximales du kart."""

    # vitesse de déplacement, m/s
    movingSpeed: float = 30
    # vitesse de rotation, rad/s
    turningSpeed: float = 1
    # vitesse d'ajustement s
    correctionSpeed: float = 1

    # -1 = en arrière, 0 = arrêté, 1 = en avant
    _moving: int

    # -1 = à droite, 0 = tout droit, 1 = à gauche
    _turning: int

    def __init__(self, **kwargs) -> None:
        super().__init__(**kwargs)
        self._angularMotion.set_center(self.center())
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

    def onEventsRegistered(self, deltaTime: float) -> None:
        self.set_angularMotionSpeed(self._turning * self.turningSpeed)
        targetSpeed = lib.Vector((self._moving * self.movingSpeed, 0))
        targetSpeed.rotate(self.angle())
        currentSpeed = self.vectorialMotionSpeed()
        acceleration = lib.Vector()
        for i in range(2):
            acceleration[i] = (targetSpeed[i] - currentSpeed[i]) / self.correctionSpeed
        self.set_vectorialMotionAcceleration(acceleration)


6
