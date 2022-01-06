import math
from typing import List
import lib

from .Polygon import Polygon
from .motions import angulars as angularMotions, vectorials as vectorialMotions


class Kart(Polygon):
    acceleration = 10
    decceleration = 30
    lossesDecceleration = 5
    turning = 1

    _accelerationsQueue: List[int]
    _turningQueue: List[int]

    def __init__(self, **kwargs) -> None:
        super().__init__(**kwargs)
        self._vectorialMotion = vectorialMotions.UniformlyAcceleratedMotion()
        self._accelerationsQueue = []
        self._turningQueue = []
        self._isTurning = 0

    def addAcceleration(self, acceleration: int) -> None:
        """Demande à change "l'accélération" du kart.
        <acceleration> fonctionnne de la manière suivante:
        -1 -> ralentir (freins / reculer), 0 -> frottements seulement, 1 -> accélérer"""
        self._accelerationsQueue.append(acceleration)

    def addTurning(self, turning: int) -> None:
        """Demande à change la "direction" du kart".
        <turning> fonctionnne de la manière suivante:
        -1 -> droite, 0 -> tout droit, 1 -> gauche"""
        self._turningQueue.append(turning)

    def updateReferences(self, deltaTime: float) -> None:
        super().updateReferences(deltaTime)