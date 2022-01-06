import lib

from .Fill import Fill

class Pattern(Fill):
    _repeat: str
    _source: str

    def __init__(self, type: str, repeat: str, sourceURL: str) -> None:
        self._type = type
        self._repeat = repeat
        self._source = sourceURL

    def type(self) -> str:
        if self._type != "Pattern":
            raise "Le pattern attendu est ""Pattern"", or celui reçu est:" + self._type
        else:
            return self._type

    def repeat(self) -> str:
        """Retourne la méthode de remplissage du pattern"""
        return self._repeat

    def source(self) -> str:
        """Retourne la source (URL) du pattern"""
        return self._source