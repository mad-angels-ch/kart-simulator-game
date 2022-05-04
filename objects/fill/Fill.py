import json
import lib


class Fill:
    """Classe abstrate indiquant la méthode de remplissage d'un objet"""

    def fromDict(fill: dict) -> "Fill":
        """Créé un objet Fill à partir d'un dict python"""
        raise "Must be overloaded"

    def type(self) -> str:
        """Retourne la méthode de remplissage de l'objet"""
        raise "Must be overloaded"

    def toDict(self) -> dict:
        """Transforme cette objet en un json et retourne"""
        return {"class": self.__class__.__name__}
