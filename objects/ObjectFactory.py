import json
from math import radians
from typing import Any, Dict, List
import lib

from .Object import Object
from .Circle import Circle
from .Polygon import Polygon
from .Flipper import Flipper
from .Kart import Kart
from .FinishLine import FinishLine
from .Lava import Lava
from .Gate import Gate
from .FireBall import FireBall

from .fill import Fill, Hex, Pattern
from .motions.angulars import (
    AngularMotion,
    UniformlyAcceleratedCircularMotion,
    AngularHarmonicMotion,
)
from .motions.vectorials import (
    VectorialMotion,
    UniformlyAcceleratedMotion,
    VectorialHarmonicMotion,
)


class ObjectFactory:
    """Classe de la factory des objects\n
    Pour chaques parties, une instance de cette classe est créé.
    La création, stockage, gestion et destruction des objects doivent impérativment se faire uniquement par cette instance."""

    maxObjectsPerGroup: int = 1000000

    _objectsCreatedCount: int
    _objectsDict: Dict[int, Object]
    _deletedObjectsDict: Dict[int, Object]
    _objectGroupCount: int

    def __init__(self, fabric: str) -> None:
        self._objectsCreatedCount = 0
        self._objectsDict = {}
        self._deletedObjectsDict = {}
        self._objectGroupCount = 0
        self._fromFabric(fabric)

    def _create(self, objectType, **kwds: Any) -> None:
        """Créé et enregistre l'objet selon les paramètres passés. Ne pas utiliser les contructeurs de ceux-ci."""
        kwds["formID"] = (
            ObjectFactory.maxObjectsPerGroup * self._objectGroupCount
            + self._objectsCreatedCount
        )
        self._objectsCreatedCount += 1

        if objectType == "Circle":
            circle = Circle(**kwds)
            self._objectsDict[circle.formID()] = circle
        elif objectType == "Polygon":
            polygon = Polygon(**kwds)
            self._objectsDict[polygon.formID()] = polygon
        elif objectType == "Flipper":
            flipper = Flipper(**kwds)
            self._objectsDict[flipper.formID()] = flipper
        elif objectType == "Lava":
            lava = Lava(**kwds)
            self._objectsDict[lava.formID()] = lava
        elif objectType == "Kart":
            kart = Kart(**kwds)
            self._objectsDict[kart.formID()] = kart
        elif objectType == "Gate":
            gate = Gate(**kwds)
            self._objectsDict[gate.formID()] = gate
        elif objectType == "FinishLine":
            finishLine = FinishLine(**kwds)
            self._objectsDict[finishLine.formID()] = finishLine
        elif objectType == "FireBall":
            fireBall = FireBall(**kwds)
            self._objectsDict[fireBall.formID()] = fireBall
        else:
            raise ValueError(f"{objectType} is not valid")

    def _fromFabric(self, fabric: str) -> None:
        """Charge un json d'un monde créé par le créateur (https://lj44.ch/creator/kart)"""
        gatesCount = 0
        finishLineCount = 0
        kartPlaceHolderCount = 0
        flippersCount = 0

        loaded = json.loads(fabric)
        jsonObjects = loaded["objects"]
        version = loaded["version"]

        if version == "4.4.0":
            for obj in jsonObjects:
                objectType = obj["type"]
                if objectType in ["circle", "LGECircle"]:
                    objectType = "Circle"
                elif objectType in ["polygon", "LGEPolygon"]:
                    objectType = "Polygon"
                elif objectType in ["LGEFlipper"]:
                    objectType = "Flipper"
                    flippersCount += 1
                elif objectType in ["LGELava"]:
                    objectType = "Lava"
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
                kwds = self._createObjectCharachteristics(
                    object=obj, objectType=objectType
                )
                self._createObjectMotions(obj=obj, objectType=objectType, kwds=kwds)
                self._create(objectType, **kwds)

        else:
            raise RuntimeError("Unsupported json version")

        if flippersCount == 0:
            if gatesCount < 2:
                raise ObjectCountError("Gate", 2, gatesCount)
            elif finishLineCount != 1:
                raise ObjectCountError("Finish line", 1, finishLineCount)
            elif kartPlaceHolderCount < 1:
                raise ObjectCountError("Kart placeholder", 1, kartPlaceHolderCount)

        self._objectGroupCount += 1

    def _get_objectType(self, object: dict) -> str:
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

    def _createObjectCharachteristics(self, object: dict, objectType: str):
        kwds = {
            "name": object["lge"].get("name"),
            "center": lib.Point((object["left"], object["top"])),
            "angle": radians(object["angle"]),
            "opacity": object["opacity"],
            "friction": object["lge"]["friction"],
            "mass": object["lge"]["mass"],
        }
        if objectType == "Lava":
            kwds["fill"] = self._fromFabricFill("#ffa500")
        else:
            kwds["fill"] = self._fromFabricFill(object["fill"])

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
            "FireBall",
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

    def _fromFabricFill(self, fabricFill: "dict | str") -> Fill:
        """Créé et retourne une méthode de remplissage à partir de la propriété 'fill' d'un objet exporté de la librairie http://fabricjs.com/."""
        if isinstance(fabricFill, str):
            if fabricFill[0] != "#":
                f = fabricFill[4:-1].split(",")
                l = list()
                for i in f:
                    l.append(int(i))
                fabricFill = "#%02x%02x%02x" % (l[0], l[1], l[2])
            return Hex(fabricFill)
        elif fabricFill["type"] == "pattern":
            return Pattern(**fabricFill)
        else:
            raise RuntimeError("jsonObject is not in a supported format")

    def _fromFabricAngularMotion(self, fabricAngle: dict) -> AngularMotion:
        """Créé et retourne le mouvement de rotation à partir du format exporté par le créateur"""
        center = lib.Point(fabricAngle["center"].values())
        if fabricAngle["type"] in ["uacm"]:
            return UniformlyAcceleratedCircularMotion(
                center, fabricAngle["velocity"], fabricAngle["acceleration"]
            )

        elif fabricAngle["type"] in ["sahm"]:
            return AngularHarmonicMotion(
                fabricAngle["period"],
                fabricAngle["amplitude"],
                fabricAngle["phase"],
                center,
            )

        else:
            return AngularMotion(fabricAngle["velocity"], center)

    def _fromFabricVectorialMotion(self, fabricVector: dict) -> VectorialMotion:
        """Créé et retourne le mouvement de translation à partir du format exporté par le créateur"""
        if fabricVector["type"] in ["uam"]:
            return UniformlyAcceleratedMotion(
                lib.Vector(fabricVector["velocity"].values()),
                lib.Vector(fabricVector["acceleration"].values()),
            )

        elif fabricVector["type"] in ["svhm"]:
            return VectorialHarmonicMotion(
                fabricVector["period"],
                lib.Vector(fabricVector["amplitude"].values()),
                fabricVector["phase"],
            )

        else:
            return VectorialMotion(lib.Vector(fabricVector["velocity"].values()))

    def _createObjectMotions(self, obj, objectType, kwds):
        if objectType in ["Kart"]:
            kwds["angularMotion"] = motions.angulars.UniformlyAcceleratedCircularMotion(
                rotationCenter=lib.Vector((-25, 0))
            )
            kwds["vectorialMotion"] = motions.vectorials.UniformlyAcceleratedMotion()
        else:
            kwds["angularMotion"] = motions.angulars.createAngularMotion._fromFabric(
                obj["lge"]["motion"]["angle"]
            )
            kwds[
                "vectorialMotion"
            ] = motions.vectorials.createVectorialMotion._fromFabric(
                obj["lge"]["motion"]["vector"]
            )
        if objectType in ["Flipper"]:
            kwds["flipperMaxAngle"] = obj["lge"]["flipperMaxAngle"]
            kwds["flipperUpwardSpeed"] = obj["lge"]["flipperUpwardSpeed"]

    def _createFromPattern(
        self,
        jsonObjects: List[dict],
        position: lib.Point = lib.Point(),
        angle: float = 0,
        version: str = "4.4.0",
    ):
        """Ajoute des objets à partir d'un nouveau json à la position 'position'."""
        self._jsonLoadedCount += 1
        if version == "4.4.0":
            for obj in jsonObjects:
                objectType = self._get_objectType(obj)
                kwds = self._createObjectCharachteristics(
                    object=obj, objectType=objectType
                )
                kwds["center"].translate(lib.Vector.fromPoints(lib.Vector(), position))
                kwds["angle"] += angle
                self._createObjectMotions(obj=obj, objectType=objectType, kwds=kwds)
                self.create(objectType, **kwds)

    def removeObjectsFromJson(self, jsonID: int):
        """Supprime tous les objets crées à partir du json dont l'id est 'jsonID'"""
        objsToDel = []
        for obj in self.objects():
            if obj.get_parentJsonID() == jsonID:
                objsToDel.append(
                    obj.formID()
                )  # Pour ne pas changer le dictionnaire lors de l'itérations sur ses éléments
        for id in objsToDel:
            self.removeObject(id)

    def removeObject(self, objectID: int):
        """Retire l'objet dont l'ID est 'ObjectID' de la liste des objets."""
        try:
            self._deletedObjectsDict[objectID] = self._objectsDict
            del self._objectsDict[objectID]
        except:
            raise ValueError("There is no object with such an ID.")

    def object(self, objectID: int) -> Object:
        try:
            return self._objectsDict[objectID]
        except:
            raise ValueError("There is no object with such an ID.")

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

    def deletedObjects(self):
        return self._deletedObjectsDict

    def loadKart(self, username: str, img: str, placeHolder: int = None) -> int:
        pass

    def unloadKart(self, placeHolder: int) -> None:
        pass

    def createFireBall(self, launcher: Kart) -> int:
        pass

    def destroyFireBall(self, id: int) -> None:
        pass


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
