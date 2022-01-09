from typing import List

import lib

from .Gate import Object, Gate, Kart


class FinishLine(Gate):

    _numberOfLaps: int

    def __init__(self, **kwargs) -> None:
        super().__init__(**kwargs)
        self._numberOfLaps = kwargs.get("numberOfLaps", 1)

    def onCollision(self, other: "Object", timeSinceLastFrame: float) -> None:
        # Ne pas compter le premier passage du la ligne d'arrivée (qui est la ligne de départ)
        if isinstance(other, Kart) and other.lastGate():
            super().onCollision(other, timeSinceLastFrame)

    def numberOfLapsRequired(self) -> int:
        """Retourne le nombre de tours de piste nécessaire pour terminer la partie"""
        return self._numberOfLaps

    def completedAllLaps(self, kartFormID: int) -> bool:
        """Retourne vrai si le kart à terminé ses tours de pistes"""
        return self.passagesCount(kartFormID) >= self._numberOfLaps
