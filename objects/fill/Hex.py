import lib

from .Fill import Fill


class Hex(Fill):
    """Remplissage uniforme de coleur exprimé en hex (ex. #000000)"""

    _value: str

    def fromDict(fill: dict) -> "Fill":
        return Hex(fill["value"])

    def __init__(self, hexColor: str) -> None:
        self._value = hexColor

    def type(self) -> str:
        return "Hex"

    def value(self) -> str:
        """Retourne la couleur (en hex) de remplissage"""
        return self._value

    def toDict(self) -> dict:
        dic = super().toDict()
        dic.update({"value": self._value})
        return dic
