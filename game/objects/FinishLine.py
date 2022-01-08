from typing import List

import lib

from .Gate import Object, Gate


class FinishLine(Gate):

    _numberOfLaps: int

    def __init__(self, **kwargs) -> None:
        super().__init__(**kwargs)
        self._numberOfLaps = kwargs.get("numberOfLaps", 1)

    def numberOfLapsRequired(self) -> int:
        """Retourne le nombre de tours de piste nécessaire pour terminer la partie"""
        return self._numberOfLaps

    def completedAllLaps(self, kartFormID: int) -> bool:
        """Retourne vrai si le kart à terminé ses tours de pistes"""
        return self.passagesCount(kartFormID) >= self._numberOfLaps
