from typing import List
import lib

from .Polygon import Polygon
from .motions import angulars as angularMotions, vectorials as vectorialMotions


class Kart(Polygon):
    _acceleration = lib.Vector((0, 10))
    _turning = 1

    _accelerationsQueue: List[int]
    _turningQueue: List[int]
    _isTurning: int

    def __init__(self, **kwargs) -> None:
        super().__init__(**kwargs)
        self.vectorialMotion = vectorialMotions.UniformlyAcceleratedMotion()
        self._accelerationsQueue = []
        self._turningQueue = []
        self._isTurning = 0

    def addAcceleration(self, acceleration: int) -> None:
        """Demande à change "l'accélération" du kart.
        <acceleration> fonctionnne de la manière suivante:
        <0 -> ralentir (freins / reculer), 0 -> frottements seulement, >0 -> accélérer"""
        self._accelerationsQueue.append(acceleration)

    def addTurning(self, turning: int) -> None:
        """Demande à change la "direction" du kart".
        <turning> fonctionnne de la manière suivante:
        <0 -> droite, 0 -> tout droit, >0 -> gauche"""
        self._turningQueue.append(turning)

    def isTurning(self) -> int:
        """Retourne -1 si le kart est en train de tourner à droite,
        0 s'il va tout droit et 1 s'il tourne à gauche"""
        return self._isTurning

    def updateReferences(self, deltaTime: float) -> None:
        super().updateReferences(deltaTime)
        while len(self._accelerationsQueue):
            acceleration = self._accelerationsQueue.pop(0)
            if acceleration > 0:
                self.set_vectorialMotionAcceleration(self._acceleration)
            elif acceleration < 0:
                self.set_vectorialMotionAcceleration(-self._acceleration)
            else:
                self.set_vectorialMotionAcceleration(lib.Vector())
        while len(self._turningQueue):
            self._isTurning = self._turningQueue.pop(0)
        if self._isTurning < 0:
            self.vectorialMotionAcceleration().rotate(-self._turning * deltaTime)
        elif self._isTurning > 0:
            self.vectorialMotionAcceleration().rotate(self._turning * deltaTime)
