import math
import inspect
from logging import warning
from typing import List

import lib

from .Polygon import Polygon


class Flipper(Polygon):
    _flipperMaxAngle: float
    _flipperUpwardSpeed: float
    _flipperCurrentAngle: float
    _flipperMovementsQueue: List[bool]

    def __init__(self) -> None:
        super().__init__()
        self._flipperMaxAngle = 0
        self._flipperUpwardSpeed = 0
        self._flipperCurrentAngle = 0
        self._flipperMovementsQueue = []

    def addMovement(self, upward: bool) -> None:
        """Ajoute un nouveau mouvement dans la file d'attente"""
        self._flipperMovementsQueue.append(upward)

    def inMotion(self) -> bool:
        """Retourne vrai si le flipper est en mouvement"""
        return not math.isclose(
            self.angularMotion.speed(), 0, abs_tol=Flipper.precision
        )

    def leftSide(self) -> bool:
        """Retourne vrai si le flipper tourne dans le sens trigonométrique lorsqu'il monte"""
        return self._flipperMaxAngle > 0

    def relativeAngle(self, deltaTime: float) -> float:
        relativeAngle = super().relativeAngle(deltaTime)
        if self.leftSide():
            if relativeAngle < 0:
                return 0
            elif relativeAngle > self._flipperMaxAngle:
                return self._flipperMaxAngle
            else:
                return relativeAngle
        else:
            if relativeAngle > 0:
                return 0
            elif relativeAngle < self._flipperMaxAngle:
                return self._flipperMaxAngle
            else:
                return relativeAngle

    def set_angle(self, newAngle: float) -> None:
        warning(f"{__name__}.set_angle() has been used")
        return super().set_angle(newAngle)

    def rotate(self, angle: float) -> None:
        self._flipperCurrentAngle += angle
        return super().rotate(angle)

    def updateReferences(self, deltaTime: float) -> None:
        super().updateReferences(deltaTime)
        if self.down():
            while len(self._flipperMovementsQueue):
                if self._flipperMovementsQueue.pop(0):
                    self.angularMotion.set_speed(self._flipperUpwardSpeed)
                    break
        elif self.up():
            while len(self._flipperMovementsQueue):
                if not self._flipperMovementsQueue.pop(0):
                    self.angularMotion.set_speed(-self._flipperUpwardSpeed)
                    break

    def up(self) -> bool:
        """Retourne vrai si le flipper est dans sa position en haut"""
        return self._flipperCurrentAngle == self._flipperMaxAngle

    def down(self) -> bool:
        """Retourne vrai si le flipper est dans sa position en bas"""
        return self._flipperCurrentAngle == 0

    def upward(self) -> bool:
        """Retourne True si le flipper est en train de monter"""
        return self.angularMotion.speed() == self._flipperUpwardSpeed

    def downward(self) -> bool:
        """Retourne True si le flipper est en train de descendre"""
        return self.angularMotion.speed() == -self._flipperUpwardSpeed
