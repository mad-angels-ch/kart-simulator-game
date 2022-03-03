import json
from math import radians
from typing import Any, Dict, List
from game.objects.FireBall import FireBall
from game.objects.motions.vectorials import *
from game.objects.motions.angulars import *
import lib

from .Object import Object
from .Circle import Circle
from .Polygon import Polygon
from .Flipper import Flipper
from .Kart import Kart
from .FinishLine import FinishLine
from .Lava import Lava
from .Gate import Gate
from . import motions
from .fill import createFill


class ObjectFactory:
    """Classe permettant la création de la factory function des objest."""
    _objectsCreatedCount: int
    _objectsDict: Dict[int, Object]
    _jsonLoadedCount: int
    
    def __init__(self) -> None:
        self._objectsCreatedCount = 0
        self._objectsDict = {}
        self._jsonLoadedCount = 0
        
    def create(self, objectType, **kwds: Any) -> Object:
        """Créé et enregistre l'objet selon les paramètres passés. Ne pas utiliser les contructeurs de ceux-ci."""
        self._objectsCreatedCount += 1
        
        kwds["formID"] = 1000000 * self._jsonLoadedCount + self._objectsCreatedCount

        if objectType == "Circle":
            circle = Circle(**kwds)
            self._objectsDict[circle.formID()] = circle
            return circle
        elif objectType == "Polygon":
            polygon = Polygon(**kwds)
            self._objectsDict[polygon.formID()] = polygon
            return polygon
        elif objectType == "Flipper":
            flipper = Flipper(**kwds)
            self._objectsDict[flipper.formID()] = flipper
            return flipper
        elif objectType == "Lava":
            lava = Lava(**kwds)
            self._objectsDict[lava.formID()] = lava
            return lava
        elif objectType == "Kart":
            kart = Kart(**kwds)
            self._objectsDict[kart.formID()] = kart
            return kart
        elif objectType == "Gate":
            gate = Gate(**kwds)
            self._objectsDict[gate.formID()] = gate
            return gate
        elif objectType == "FinishLine":
            finishLine = FinishLine(**kwds)
            self._objectsDict[finishLine.formID()] = finishLine
            return finishLine
        elif objectType == "FireBall":
            fireBall = FireBall(**kwds)
            self._objectsDict[fireBall.formID()] = fireBall
            return fireBall
        else:
            raise ValueError(f"{objectType} is not valid")
    

    def fromFabric(
        self, jsonObjects: List[dict], version: str = "4.4.0"
    ) -> List[Object]:
        """Charge et retourne les objets selon le json créé par le créateur.\n
        La création de ce json est basé sur http://fabricjs.com/ avec des ajouts sous la propriété 'lge'."""
        self._jsonLoadedCount += 1
        self.gatesCount = 0
        self.finishLineCount = 0
        self.kartPlaceHolderCount = 0
        self.flippersCount = 0
        
        if version == "4.4.0":
            for obj in jsonObjects:
                objectType = self.get_objectType(obj)
                kwds = self.createObjectCharachteristics(object=obj, objectType=objectType)
                self.createObjectMotions(obj=obj, objectType=objectType, kwds=kwds)
                self.create(objectType, **kwds)

        if not self.flippersCount:
            if self.gatesCount < 2:
                raise ObjectCountError("Gate", 2, self.gatesCount)
            elif self.finishLineCount != 1:
                raise ObjectCountError("Finish line", 1, self.finishLineCount)
            elif self.kartPlaceHolderCount < 1:
                raise ObjectCountError("Kart placeholder", 1, self.kartPlaceHolderCount)
        
        
        return self._objectsDict.values()
        
        
    def get_objectType(self, object: dict):
        objectType = object["type"]
        if objectType in ["circle", "LGECircle"]:
            objectType = "Circle"
        elif objectType in ["polygon", "LGEPolygon"]:
            objectType = "Polygon"
        elif objectType in ["LGEFlipper"]:
            objectType = "Flipper"
            self.flippersCount += 1
        elif objectType in ["LGELava"]:
            objectType = "Lava"
        elif objectType in ["LGEKartPlaceHolder"]:
            objectType = "Kart"
            self.kartPlaceHolderCount += 1
        elif objectType in ["LGEGate"]:
            objectType = "Gate"
            self.gatesCount += 1
        elif objectType in ["LGEFinishLine"]:
            objectType = "FinishLine"
            self.gatesCount += 1
            self.finishLineCount += 1
        return objectType
    
    
    def createObjectCharachteristics(self, object: dict, objectType: str):
        kwds = {
            "name": object["lge"].get("name"),
            "center": lib.Point((object["left"], object["top"])),
            "angle": radians(object["angle"]),
            "opacity": object["opacity"],
            "friction": object["lge"]["friction"],
            "mass": object["lge"]["mass"],
        }
        if objectType == "Lava":
            kwds["fill"] = createFill.fromFabric("#ffa500")
        else:
            kwds["fill"] = createFill.fromFabric(object["fill"])

        scaleX, scaleY = object["scaleX"], object["scaleY"]

        if object["flipX"]:
            scaleX *= -1
        if object["flipY"]:
            scaleY *= -1

        if objectType in ["Circle"]:
            kwds["radius"] = object["radius"] * min(scaleX, scaleY)

        if objectType in [
            "Polygon",
            "Flipper",
            "Kart",
            "Gate",
            "FinishLine",
            "Lava",
            "FireBall"
        ]:
            kwds["vertices"] = [
                lib.Point((point["x"], point["y"])) for point in object["points"]
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

            if objectType in ["FinishLine"]:
                kwds["numberOfLaps"] = object["lge"]["numberOfLaps"]

            elif objectType in ["Kart"]:
                kwds["vertices"] = [
                    lib.Vector((-25, -8)),
                    lib.Vector((-25, 8)),
                    lib.Vector((25, 8)),
                    lib.Vector((25, -8)),
                ]
        return kwds
    
    def createObjectMotions(self, obj, objectType, kwds):
        if objectType in ["Kart"]:
            kwds[
                "angularMotion"
            ] = motions.angulars.UniformlyAcceleratedCircularMotion(
                rotationCenter=lib.Vector((-25, 0))
            )
            kwds[
                "vectorialMotion"
            ] = motions.vectorials.UniformlyAcceleratedMotion()
        else:
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
        if objectType in ["Flipper"]:
            kwds["flipperMaxAngle"] = obj["lge"]["flipperMaxAngle"]
            kwds["flipperUpwardSpeed"] = obj["lge"]["flipperUpwardSpeed"]


    def createFromPattern(self, jsonObjects: List[dict], position: lib.Point = lib.Point(), angle: float = 0, vectorialMotion: VectorialMotion = None, angularMotion: AngularMotion = None, version: str = "4.4.0"):
        """Ajoute des objets à partir d'un nouveau json à la position 'position'"""
        self._jsonLoadedCount += 1
        if version == "4.4.0":
            for obj in jsonObjects:
                objectType = self.get_objectType(obj)
                kwds = self.createObjectCharachteristics(object=obj, objectType=objectType)
                kwds["center"] += position
                kwds["angle"] += angle
                obj = self.create(objectType, **kwds)
                if vectorialMotion:
                    obj._vectorialMotion = vectorialMotion
                if angularMotion:
                    obj._angularMotion = angularMotion

    def deleteObjectsFromJson(self, jsonID: int):
        """Supprime tous les objets crées à partir du json dont l'id est 'jsonID'"""
        for obj in self.objects():
            if str(obj.formID())[0] == jsonID:
                self.removeObject(obj.formID())

    def clearAll(self):
        """Remet à zéro la factory, c'est-à-dire retire tous les objets de la liste d'objets et remet le décompte du nombre d'objets à zéro."""
        self._objectsCreatedCount = 0
        self._objectsDict = {}
    
    def removeObject(self, objectID: int):
        """Retire l'objet dont l'ID est 'ObjectID' de la liste des objets."""
        del self._objectsDict[objectID]

    def objectsDict(self):
        return self._objectsDict
    
    def objects(self):
        return self._objectsDict.values()

    def objectsByType(self, type):
        listobj = []
        for obj in self.objects():
            if isinstance(obj, type):
                listobj.append(obj)
        return listobj
    
    
    
class ObjectCountError(RuntimeError):
    """Classe pour les erreurs dans le fabric json."""

    _type: str
    _requiredCount: int
    _foundCount: int

    def __init__(self, objectType: str, requiredCount: int, foundCount: int) -> None:
        self._type = objectType
        self._requiredCount = requiredCount
        self._foundCount = foundCount

    def message(self) -> str:
        """Message de l'erreur."""
        if self._requiredCount == 1:
            if self._foundCount == 1:
                return f"{self._requiredCount} {self._type} was expected but {self._foundCount} was found"
            else:
                return f"{self._requiredCount} {self._type} was expected but {self._foundCount} were found"
        else:
            if self._foundCount == 1:
                return f"{self._requiredCount} {self._type} were expected but {self._foundCount} was found"
            else:
                return f"{self._requiredCount} {self._type} were expected but {self._foundCount} were found"


create = ObjectFactory()
