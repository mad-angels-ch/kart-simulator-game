from .Gate import Object, Gate, Kart, Polygon


class FinishLine(Gate):
    """Classe de la ligne d'arrivée."""

    _numberOfLaps: int
    _highestPosition: int

    def __init__(self, **kwargs) -> None:
        super().__init__(**kwargs)
        self._position = 0
        self._numberOfLaps = kwargs["numberOfLaps"]
        self._highestPosition = kwargs.get("highestPosition", 1)

    def isNextGate(self, kart: Kart) -> bool:
        return kart.lastGatePosition() == self.highestPosition()

    def numberOfLapsRequired(self) -> int:
        """Retourne le nombre de tours de piste nécessaire pour terminer la partie"""
        return self._numberOfLaps

    def numberOfGates(self) -> int:
        """Retourne le nombre de portillons du circuit. Deux portillons avec la même position sont compté comme un"""
        return self._highestPosition + 1

    def highestPosition(self) -> int:
        """Retourne la position du dernier portillons à passer avant la ligne d'arrivée"""
        return self._highestPosition

    def set_highestPosition(self, highestPosition: int) -> None:
        """Nom explicite"""
        self._highestPosition = highestPosition

    def completedAllLaps(self, kartFormID: int) -> bool:
        """Retourne vrai si le kart à terminé ses tours de pistes"""
        return self.passagesCount(kartFormID) >= self._numberOfLaps

    def toMinimalDict(self) -> dict:
        dic = super().toMinimalDict()
        dic.update(
            {
                "numberOfLaps": self._numberOfLaps,
                "highestPosition": self._highestPosition,
            }
        )
        return dic
