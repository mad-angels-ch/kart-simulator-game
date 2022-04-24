from typing import Callable, Dict

from .Polygon import Object, Polygon
from .Kart import Kart


onPassageT = Callable[["Gate", Kart], None]


class Gate(Polygon):
    """Classe des portillons, un objet qui compte le nombre de passage des karts.
    Un minimum de deux portillons (ou de classes dérivées) sont nécessaire pour un fonctionnement correct."""

    _passagesCount: Dict[int, int]
    _onPassage: onPassageT

    def __init__(self, **kwargs) -> None:
        kwargs["isSolid"] = False
        super().__init__(**kwargs)
        self._passagesCount = kwargs.get("passagesCount", {})

    def onCollision(self, other: "Object") -> None:
        super().onCollision(other)
        if isinstance(other, Kart) and other.lastGate() != self.formID():
            self._passagesCount[other.formID()] = (
                self._passagesCount.get(other.formID(), 0) + 1
            )
            other.set_lastGate(self)

    def passagesCount(self, kartFormID: int) -> int:
        """Indique le nombre de fois que le kart a franchi le portillon"""
        return self._passagesCount.get(kartFormID, 0)

    def toMinimalDict(self) -> dict:
        dic = super().toMinimalDict()
        dic.update({"passagesCount": self._passagesCount})
        return dic
