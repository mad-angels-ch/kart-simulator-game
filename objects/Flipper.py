import math
import inspect
from logging import warning
from typing import List

import lib

from .Polygon import Polygon


class Flipper(Polygon):
    """Classe des flippers, uniquement pour l'easter egg (à vous de le trouver!)"""

    _flipperMaxAngle: float
    _flipperUpwardSpeed: float
    _flipperCurrentAngle: float
    _flipperMovementsQueue: List[bool]

    def __init__(self, **kwargs) -> None:
        super().__init__(**kwargs)
        self._flipperMaxAngle = kwargs["flipperMaxAngle"]
        self._flipperUpwardSpeed = kwargs["flipperUpwardSpeed"]
        self._flipperCurrentAngle = 0
        self._flipperMovementsQueue = []
        self._name = kwargs["name"]



    def name(self) -> str:
        """Retourne le nom de l'objet.\n
        Ne correspond pas à la classe, mais à la fonction du flipper "rightFlipper" ou "leftFlipper"."""
        return self._name
    
    def addMovement(self, upward: bool) -> None:
        """Ajoute un nouveau mouvement dans la file d'attente"""
        self._flipperMovementsQueue.append(upward)

    def inMotion(self) -> bool:
        """Retourne vrai si le flipper est en mouvement"""
        return not math.isclose(self.angularMotionSpeed(), 0, abs_tol=Flipper.precision)

    def leftSide(self) -> bool:
        """Retourne vrai si le flipper tourne dans le sens trigonométrique lorsqu'il monte"""
        return self._flipperMaxAngle > 0

    def relativeAngle(self, deltaTime: float) -> float:
        relativeAngle = super().relativeAngle(deltaTime)
        if self.leftSide():
            if (
                self.upward()
                and self._flipperCurrentAngle + relativeAngle >= self._flipperMaxAngle
            ):
                return self._flipperMaxAngle - self._flipperCurrentAngle
            elif self.downward() and self._flipperCurrentAngle - relativeAngle <= 0:
                return -self._flipperCurrentAngle
            else:
                return relativeAngle
        else:
            if (
                self.upward()
                and self._flipperCurrentAngle + relativeAngle <= self._flipperMaxAngle
            ):
                return self._flipperMaxAngle - self._flipperCurrentAngle
            elif self.downward() and self._flipperCurrentAngle - relativeAngle >= 0:
                return -self._flipperCurrentAngle
            else:
                return relativeAngle

    def set_angle(self, newAngle: float) -> None:
        self._flipperCurrentAngle += newAngle - self.angle()
        return super().set_angle(newAngle)

    def rotate(self, angle: float) -> None:
        self._flipperCurrentAngle += angle
        return super().rotate(angle)

    def onEventsRegistered(self, deltaTime: float) -> None:
        # fin de trajectoire
        if (self.upward() and self._flipperCurrentAngle == self._flipperMaxAngle) or (
            self.downward() and self._flipperCurrentAngle == 0
        ):
            self.set_angularMotionSpeed(0)

        # nouvelle trajectoire
        if self.down():
            while len(self._flipperMovementsQueue):
                if self._flipperMovementsQueue.pop(0):
                    self.set_angularMotionSpeed(self._flipperUpwardSpeed)
                    break
        elif self.up():
            while len(self._flipperMovementsQueue):
                if not self._flipperMovementsQueue.pop(0):
                    self.set_angularMotionSpeed(-self._flipperUpwardSpeed)
                    break

    def up(self) -> bool:
        """Retourne vrai si le flipper est dans sa position en haut"""
        return (
            self._flipperCurrentAngle == self._flipperMaxAngle
            and self.angularMotionSpeed() == 0
        )

    def down(self) -> bool:
        """Retourne vrai si le flipper est dans sa position en bas"""
        return self._flipperCurrentAngle == 0 and self.angularMotionSpeed() == 0

    def upward(self) -> bool:
        """Retourne True si le flipper est en train de monter"""
        return self.angularMotionSpeed() == self._flipperUpwardSpeed

    def downward(self) -> bool:
        """Retourne True si le flipper est en train de descendre"""
        return self.angularMotionSpeed() == -self._flipperUpwardSpeed
