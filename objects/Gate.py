from typing import Callable, Dict

from .Polygon import Object, Polygon
from .Kart import Kart


onPassageT = Callable[["Gate", Kart], None]


class Gate(Polygon):
    """Classe des portillons, un objet qui compte le nombre de passage des karts.
    Un minimum de deux portillons (ou de classes dérivées) sont nécessaire pour un fonctionnement correct."""

    _passagesCount: Dict[int, int]
    _onPassage: onPassageT
    _position: int

    def fromMinimalDict(obj: dict) -> dict:
        dic = Polygon.fromMinimalDict(obj=obj)
        dic.update({"onPassage": lambda g, k: None})
        return dic

    def __init__(self, **kwargs) -> None:
        kwargs["isSolid"] = False
        self._position = kwargs.get("position", 1)
        self._onPassage = kwargs["onPassage"]
        super().__init__(**kwargs)
        self._passagesCount = kwargs.get("passagesCount", {})

    def isNextGate(self, kart: Kart) -> bool:
        """Retourne True si le prochain portillons que le kart doit franchir est celui-ci"""
        return kart.lastGatePosition() + 1 == self.position()

    def collides(self, other: "Object", timeInterval: float) -> bool:
        if isinstance(other, Kart) and self.isNextGate(other):
            return super().collides(other, timeInterval)
        else:
            return False

    def onCollision(self, other: "Object") -> None:
        super().onCollision(other)
        if isinstance(other, Kart) and self.isNextGate(other):
            self._passagesCount[other.formID()] = (
                self._passagesCount.get(other.formID(), 0) + 1
            )
            other.set_lastGate(self)
            self._onPassage(self, other)

    def passagesCount(self, kartFormID: int) -> int:
        """Indique le nombre de fois que le kart a franchi le portillon"""
        return self._passagesCount.get(kartFormID, 0)

    def set_passagesCount(self, kartFormID: int, passagesCount: int) -> None:
        """Permet de modifier le nombre de fois que le kart donné a franchi le portillon"""
        self._passagesCount[kartFormID] = passagesCount

    def position(self) -> int:
        """Retourne la position du portillon.\n
        Les karts doivent franchirs les portillons dans l'ordre de leurs positions.
        Si deux portillons ont la même position, ils sont considéré comme un unique portillons,
        c'est à dire que les karts doivent franchir soit l'un, soit l'autre."""
        return self._position

    def toMinimalDict(self) -> dict:
        dic = super().toMinimalDict()
        dic.update({"passagesCount": self._passagesCount})
        return dic
