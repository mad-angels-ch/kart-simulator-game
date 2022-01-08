from typing import Any

import lib

from .Fill import Fill
from .Hex import Hex
from .Pattern import Pattern


class FillFactory:
    def __call__(self, **kwds: Any) -> Any:
        if kwds["type"] == "Hex":
            return Hex(**kwds)
        elif kwds["type"] == "Pattern":
            return Pattern(**kwds)
        else:
            raise ValueError(f"{kwds['type']} is not a valide type")

    def fromFabric(self, jsonObject) -> Fill:
        kwds = {}
        if isinstance(jsonObject, str):
            kwds["type"] = "Hex"
            kwds["hexColor"] = jsonObject
            if jsonObject[0] != "#":
                f = jsonObject[4:-1].split(",")
                l = list()
                for i in f:
                    l.append(int(i))
                kwds["hexColor"] = "#%02x%02x%02x" % (l[0], l[1], l[2])
        elif jsonObject["type"] == "pattern":
            kwds["type"] = "Pattern"
            kwds["repeat"] = jsonObject["repeat"]
            kwds["sourceURL"] = jsonObject["source"]
        else:
            raise RuntimeError("jsonObject is not in a supported format")

        return self.__call__(**kwds)


createFill = FillFactory()
