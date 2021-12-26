import lib

from .Fill import Fill

class Hex(Fill):
    _value: str

    def __init__(self, hexColor: str) -> None:
        self._value = hexColor

    def type(self) -> str:
        return "Hex"

    def value(self) -> str:
        """Retourne la couleur (en hex) de remplissage"""
        return self._value