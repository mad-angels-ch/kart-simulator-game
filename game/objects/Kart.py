from typing import List
import lib

from .Polygon import Polygon
from .motions import angulars as angularMotions, vectorials as vectorialMotions


class Kart(Polygon):
    _acceleration = lib.Vector((0, 1))

    _accelerationsQueue: List[int]
    _turningQueue: List[int]

    def __init__(self) -> None:
        super().__init__()
        self._accelerationsQueue = []
        self._turningQueue = []
        self.angularMotion = angularMotions.AngularMotion()
        self.vectorialMotion = vectorialMotions.UniformlyAcceleratedMotion()

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

    def updateReferences(self, deltaTime: float) -> None:
        super().updateReferences(deltaTime)
        while len(self._accelerationsQueue):
            acceleration = self._accelerationsQueue.pop(0)
            if acceleration > 0:
                self.vectorialMotion.set_acceleration(self._acceleration)
            elif acceleration < 0:
                self.vectorialMotion.set_acceleration(-self._acceleration)
            else:
                self.vectorialMotion.set_acceleration(lib.Vector(0, 0))
        while len(self._turningQueue):
            turning = self._turningQueue.pop(0)
            if turning > 0:
                pass
