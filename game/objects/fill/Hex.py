import lib

from .Fill import Fill

class Hex(Fill):
    _value: str

    def __init__(self, type: str, hexColor: str) -> None:
        self._type = type
        self._value = hexColor

    def type(self) -> str:
        if self._type != "Hex":
            raise "Le pattern attendu est ""Pattern"", or celui reçu est:" + self._type
        else:
            return self._type

    def value(self) -> str:
        """Retourne la couleur (en hex) de remplissage"""
        return self._value