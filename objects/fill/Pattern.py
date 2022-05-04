import lib

from .Fill import Fill


class Pattern(Fill):
    """Remplissage selon un pattern, tel un répétition d'une image"""

    _repeat: str
    _source: str

    def fromDict(fill: dict) -> "Fill":
        return Pattern(fill["repeat"], fill["source"])

    def __init__(self, repeat: str, sourceURL: str) -> None:
        self._repeat = repeat
        self._source = sourceURL

    def type(self) -> str:
        return "Pattern"

    def repeat(self) -> str:
        """Retourne la méthode de remplissage du pattern"""
        return self._repeat

    def source(self) -> str:
        """Retourne la source (URL) de l'image"""
        return self._source

    def toDict(self) -> dict:
        dic = super().toDict()
        dic.update({"repeat": self._repeat, "source": self._source})
        return dic
