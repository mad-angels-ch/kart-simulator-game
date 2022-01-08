from math import radians
from typing import Any, List
from game.objects.FinishLine import FinishLine

import lib

from .Object import Object
from .Circle import Circle
from .Polygon import Polygon
from .Flipper import Flipper
from .Kart import Kart
from .FinishLine import FinishLine
from .Gate import Gate
from . import motions
from .fill import createFill


class ObjectFactory:
    objectsCreatedCount = 0

    def __call__(self, objectType, **kwds: Any) -> Object:
        ObjectFactory.objectsCreatedCount += 1

        kwds["formID"] = ObjectFactory.objectsCreatedCount

        if objectType == "Circle":
            return Circle(**kwds)
        elif objectType == "Polygon":
            return Polygon(**kwds)
        elif objectType == "Flipper":
            return Flipper(**kwds)
        elif objectType == "Kart":
            return Kart(**kwds)
        elif objectType == "Gate":
            return Gate(**kwds)
        elif objectType == "FinishLine":
            return FinishLine(**kwds)
        else:
            raise ValueError(f"{objectType} is not valid")

    def fromFabric(
        self, jsonObjects: List[dict], version: str = "4.4.0"
    ) -> List[Object]:
        gatesCount = 0
        finishLineCount = 0
        kartPlaceHolderCount = 0

        newObjects = []
        if version == "4.4.0":
            for obj in jsonObjects:
                objectType = obj["type"]
                if objectType in ["circle", "LGECircle"]:
                    objectType = "Circle"
                elif objectType in ["polygon", "LGEPolygon"]:
                    objectType = "Polygon"
                elif objectType in ["LGEFlipper"]:
                    objectType = "Flipper"
                elif objectType in ["LGEKartPlaceHolder"]:
                    objectType = "Kart"
                    kartPlaceHolderCount += 1
                elif objectType in ["LGEGate"]:
                    objectType = "Gate"
                    gatesCount += 1
                elif objectType in ["LGEFinishLine"]:
                    objectType = "FinishLine"
                    gatesCount += 1
                    finishLineCount += 1

                kwds = {
                    "name": obj["lge"].get("name"),
                    "center": lib.Point((obj["left"], obj["top"])),
                    "angle": radians(obj["angle"]),
                    "fill": createFill.fromFabric(obj["fill"]),
                    "opacity": obj["opacity"],
                    "friction": obj["lge"]["friction"],
                    "mass": obj["lge"]["mass"],
                }
                if objectType != "FinishLine":
                    scaleX, scaleY = obj["scaleX"], obj["scaleY"]
                if obj["flipX"]:
                    scaleX *= -1
                if obj["flipY"]:
                    scaleY *= -1

                if objectType in ["Circle"]:
                    kwds["radius"] = obj["radius"] * min(scaleX, scaleY)

                if objectType in ["Polygon", "Flipper", "Kart", "Gate", "FinishLine"]:
                    kwds["vertices"] = [
                        lib.Point((point["x"], point["y"])) for point in obj["points"]
                    ]
                    abscissas = [point[0] for point in kwds["vertices"]]
                    ordinates = [point[1] for point in kwds["vertices"]]

                    toOrigin = -lib.Vector(
                        (
                            (min(abscissas) + max(abscissas)) / 2,
                            (min(ordinates) + max(ordinates)) / 2,
                        )
                    )

                    for i in range(len(kwds["vertices"])):
                        kwds["vertices"][i].translate(toOrigin)
                        pointV = lib.Vector(kwds["vertices"][i])

                        pointV.scaleX(scaleX)
                        pointV.scaleY(scaleY)

                        kwds["vertices"][i] = pointV

                if objectType in ["Flipper"]:
                    kwds["flipperMaxAngle"] = obj["lge"]["flipperMaxAngle"]
                    kwds["flipperUpwardSpeed"] = obj["lge"]["flipperUpwardSpeed"]

                if objectType not in ["Kart"]:
                    kwds[
                        "angularMotion"
                    ] = motions.angulars.createAngularMotion.fromFabric(
                        obj["lge"]["motion"]["angle"]
                    )
                    kwds[
                        "vectorialMotion"
                    ] = motions.vectorials.createVectorialMotion.fromFabric(
                        obj["lge"]["motion"]["vector"]
                    )

                newObjects.append(self(objectType, **kwds))

        if gatesCount < 2:
            raise ObjectCountError("Gate", 2, gatesCount)
        elif finishLineCount < 1:
            raise ObjectCountError("Finish line", 1, finishLineCount)
        elif kartPlaceHolderCount < 1:
            raise ObjectCountError("Kart placeholder", 1, kartPlaceHolderCount)

        return newObjects


class ObjectCountError(RuntimeError):
    _type: str
    _requiredCount: int
    _foundCount: int

    def __init__(self, objectType: str, requiredCount: int, foundCount: int) -> None:
        self._type = objectType
        self._requiredCount = requiredCount
        self._foundCount = foundCount

    def message(self) -> str:
        return f"Nous attendions {self._requiredCount} {self._type} mais trouver seulemenent {self._foundCount}"


create = ObjectFactory()
