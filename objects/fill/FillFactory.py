from typing import Any

import lib

from .Fill import Fill
from .Hex import Hex
from .Pattern import Pattern


class FillFactory:
    """Factory function simplifiant la création des classes filles de Fill.
    Utiliser uniquement cette méthode pour la création de celle-ci."""

    def __call__(self, type: str, **kwds: Any) -> Any:
        """Créé et retourne à partir des argments donnés la méthode de remplissage correspondante."""
        if type == "Hex":
            return Hex(**kwds)
        elif type == "Pattern":
            return Pattern(**kwds)
        else:
            raise ValueError(f"{type} is not a valide type")

    def fromFabric(self, jsonObject) -> Fill:
        """Créé et retourne une méthode de remplissage à partir de la propriété 'fill' d'un objet exporté de la librairie http://fabricjs.com/."""
        kwds = {}
        if isinstance(jsonObject, str):
            type = "Hex"
            kwds["hexColor"] = jsonObject
            if jsonObject[0] != "#":
                f = jsonObject[4:-1].split(",")
                l = list()
                for i in f:
                    l.append(int(i))
                kwds["hexColor"] = "#%02x%02x%02x" % (l[0], l[1], l[2])
        elif jsonObject["type"] == "pattern":
            type = "Pattern"
            kwds["repeat"] = jsonObject["repeat"]
            kwds["sourceURL"] = jsonObject["source"]
        else:
            raise RuntimeError("jsonObject is not in a supported format")

        return self.__call__(type, **kwds)


createFill = FillFactory()
