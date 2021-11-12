from typing import List
import lib

from .Circle import Circle
from .motions import vectorials


class Kart(Circle):
    _accelerationsQueue: List[int]
    _turningQueue: List[int]

    def __init__(self) -> None:
        super().__init__()
        self._accelerationsQueue = []
        self._turningQueue = []

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
