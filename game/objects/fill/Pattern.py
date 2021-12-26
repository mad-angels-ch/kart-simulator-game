import lib

from .Fill import Fill

class Pattern(Fill):
    _repeat: str
    _source: str

    def __init__(self, repeat: str, sourceURL: str) -> None:
        self._repeat = repeat
        self._source = sourceURL

    def type(self) -> str:
        return "Pattern"

    def repeat(self) -> str:
        """Retourne la méthode de remplissage du pattern"""
        return self._repeat

    def source(self) -> str:
        """Retourne la source (URL) du pattern"""
        return self._source