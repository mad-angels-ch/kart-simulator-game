import json
from math import radians
from typing import Any, Dict, List
import lib

from .Object import Object
from .Circle import Circle
from .Polygon import Polygon
from .Flipper import Flipper
from .Kart import Kart, onBurnedT, onCompletedAllLapsT
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
    objectsClasses = {
        c.__name__: c
        for c in [Circle, Polygon, Flipper, Kart, FinishLine, Lava, Gate, FireBall]
    }
    fabricClassMapping = {
        "circle": Circle,
        "LGECircle": Circle,
        "polygon": Polygon,
        "LGEPolygon": Polygon,
        "LGEFlipper": Flipper,
        "LGELava": Lava,
        "LGEKartPlaceHolder": Kart,
        "LGEGate": Gate,
        "LGEFinishLine": FinishLine,
    }

    _currentGroup: int = 1
    _currentIndex: int = 1

    _objects: Dict[int, Object]
    _destroyedObjects: Dict[int, Object]
    _kartPlaceHolders: Dict[int, Kart]
    _finishLine: FinishLine

    _kart_onBurned: onBurnedT
    _kart_onCompletedAllLaps: onCompletedAllLapsT

    def __init__(
        self,
        fabric: str,
        kart_onBurned: onBurnedT,
        kart_onCompletedAllLaps: onCompletedAllLapsT,
    ) -> None:
        self._kart_onBurned = kart_onBurned
        self._kart_onCompletedAllLaps = kart_onCompletedAllLaps
        self._objects = {}
        self._destroyedObjects = {}
        self._kartPlaceHolders = {}
        if len(fabric) > 0:
            self._fromFabric(fabric)

    def _nextGroup(self) -> None:
        """Ferme le group actuel et prépare le suivant"""
        self._currentGroup += 1
        self._currentIndex = 1

    def _create(self, objectClass, **kwds: Any) -> None:
        """Créé et enregistre l'objet selon les paramètres passés. Ne pas utiliser les contructeurs de ceux-ci."""
        formID = self.maxObjectsPerGroup * self._currentGroup + self._currentIndex
        obj = objectClass(formID=formID, **kwds)
        if isinstance(obj, Kart):
            self._kartPlaceHolders[formID] = obj
        else:
            self._objects[formID] = obj
        if isinstance(obj, FinishLine):
            self._finishLine = obj
        self._currentIndex += 1

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
                try:
                    objectClass = self.fabricClassMapping[obj["type"]]
                except KeyError:
                    # pour garde la compatibilité en cas d'ajout d'une nouvelle classe
                    continue
                if issubclass(objectClass, Flipper):
                    flippersCount += 1
                elif issubclass(objectClass, Kart):
                    kartPlaceHolderCount += 1
                elif issubclass(objectClass, Gate):
                    gatesCount += 1
                    if issubclass(objectClass, FinishLine):
                        finishLineCount += 1
                self._create(objectClass, **self._fromFabricObject(objectClass, obj))

        else:
            raise RuntimeError("Unsupported json version")

        if flippersCount == 0:
            if gatesCount < 2:
                raise ObjectCountError("Gate", 2, gatesCount)
            elif finishLineCount != 1:
                raise ObjectCountError("Finish line", 1, finishLineCount)
            elif kartPlaceHolderCount < 1:
                raise ObjectCountError("Kart placeholder", 1, kartPlaceHolderCount)

        self._nextGroup()

    def _fromFabricObject(self, objectClass, objectDict: dict) -> dict:
        """Créé un dict à partir d'un object fabric tel qu'attendu par _create"""
        properties = {
            "name": objectDict["lge"].get("name"),
            "center": lib.Point((objectDict["left"], objectDict["top"])),
            "angle": radians(objectDict["angle"]),
            "opacity": objectDict["opacity"],
            "friction": objectDict["lge"]["friction"],
            "mass": objectDict["lge"]["mass"],
        }

        if issubclass(objectClass, Lava):
            properties["fill"] = self._fromFabricFill("#ffa500")
        else:
            properties["fill"] = self._fromFabricFill(objectDict["fill"])

        scaleX, scaleY = objectDict["scaleX"], objectDict["scaleY"]
        if objectDict["flipX"]:
            scaleX *= -1
        if objectDict["flipY"]:
            scaleY *= -1

        if issubclass(objectClass, Circle):
            properties["radius"] = objectDict["radius"] * min(scaleX, scaleY)

        elif issubclass(objectClass, Polygon):
            properties["vertices"] = [
                lib.Point((point["x"], point["y"])) for point in objectDict["points"]
            ]
            abscissas = [point[0] for point in properties["vertices"]]
            ordinates = [point[1] for point in properties["vertices"]]

            toOrigin = -lib.Vector(
                (
                    (min(abscissas) + max(abscissas)) / 2,
                    (min(ordinates) + max(ordinates)) / 2,
                )
            )

            for i in range(len(properties["vertices"])):
                properties["vertices"][i].translate(toOrigin)
                pointV = lib.Vector(properties["vertices"][i])

                pointV.scaleX(scaleX)
                pointV.scaleY(scaleY)

                properties["vertices"][i] = pointV

            if issubclass(objectClass, FinishLine):
                properties["numberOfLaps"] = objectDict["lge"]["numberOfLaps"]

            elif issubclass(objectClass, Kart):
                properties["vertices"] = [
                    lib.Vector((-25, -8)),
                    lib.Vector((-25, 8)),
                    lib.Vector((25, 8)),
                    lib.Vector((25, -8)),
                ]
                properties["onBurned"] = self._kart_onBurned
                properties["onCompletedAllLaps"] = self._kart_onCompletedAllLaps

            elif issubclass(objectClass, Flipper):
                properties["flipperMaxAngle"] = objectDict["lge"]["flipperMaxAngle"]
                properties["flipperUpwardSpeed"] = objectDict["lge"][
                    "flipperUpwardSpeed"
                ]

        if issubclass(objectClass, Kart):
            properties["angularMotion"] = UniformlyAcceleratedCircularMotion(
                rotationCenter=lib.Vector((-25, 0))
            )
            properties["vectorialMotion"] = UniformlyAcceleratedMotion()

        else:
            properties["angularMotion"] = self._fromFabricAngularMotion(
                objectDict["lge"]["motion"]["angle"]
            )
            properties["vectorialMotion"] = self._fromFabricVectorialMotion(
                objectDict["lge"]["motion"]["vector"]
            )

        return properties

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
            return Pattern(fabricFill["repeat"], fabricFill["source"])
        else:
            raise RuntimeError("jsonObject is not in a supported format")

    def _fromFabricAngularMotion(self, fabricAngle: dict) -> AngularMotion:
        """Créé et retourne le mouvement de rotation à partir du format exporté par le créateur"""
        center = lib.Point(list(fabricAngle["center"].values()))
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
                lib.Vector(list(fabricVector["velocity"].values())),
                lib.Vector(list(fabricVector["acceleration"].values())),
            )

        elif fabricVector["type"] in ["svhm"]:
            return VectorialHarmonicMotion(
                fabricVector["period"],
                lib.Vector(list(fabricVector["amplitude"].values())),
                fabricVector["phase"],
            )

        else:
            return VectorialMotion(lib.Vector(list(fabricVector["velocity"].values())))

    def destroyGroup(self, groupID: int) -> None:
        """Supprime tous les objets appartenant au groupe"""
        for obj in [o for o in self._objects.values() if o.groupID() == groupID]:
            obj.destroy()

    def get(self, formID: int, default: Any) -> "Object | Any":
        return self._objects.get(formID, default)

    def objects(self) -> List[Object]:
        return self._objects.values()

    def deletedObjects(self):
        return self._destroyedObjects.values()

    def kartPlaceholders(self) -> List[Kart]:
        """Retourne la liste des karts placeholder"""
        return self._kartPlaceHolders.values()

    def loadKart(self, username: str, img: str, placeHolder: int = None) -> int:
        """Créé un kart à l'emplacement donné par le placeHolder.
        Si le placeHolder n'est pas donné, il est séléctionné au hasard parmis les restants"""
        if placeHolder == None:
            placeHolder = list(self._kartPlaceHolders.keys())[0]

        kart = self._kartPlaceHolders.pop(placeHolder)
        kart.set_username(username)
        kart.set_image(img)
        self._objects[placeHolder] = kart
        return placeHolder

    def unloadKart(self, placeHolder: int) -> None:
        """Supprime le kart du jeu, peut à tout moment être recréé avec loadKart()"""
        kart = self._objects[placeHolder]
        if not isinstance(kart, Kart):
            raise RuntimeError("Invalid placeHolder")
        kart.destroy()

    def burnedKarts(self) -> List[Kart]:
        """Retourne tous les karts brûlés"""
        return [kart for kart in self._kartPlaceHolders.values() if kart.hasBurned()]

    def createFireBall(self, launcher: int) -> int:
        """Fait lancer au kart une boule de feu"""
        kart = self._objects[launcher]
        kartSpeed = kart.speed()
        baseVSpeed = lib.Vector((FireBall.baseSpeed, 0))
        baseVSpeed.rotate(kartSpeed.direction())

        ballSpeed = kartSpeed + baseVSpeed
        ballCenter = lib.Point(kart.center())
        ballCenter.translate(kartSpeed.unitVector() * FireBall.spawnDistance)

        self._create(
            FireBall, center=ballCenter, vectorialMotion=VectorialMotion(ballSpeed)
        )
        self._nextGroup()
        kart.add_fireBall()

    def __getitem__(self, formID: int) -> Object:
        """Retourne l'objet correspondant"""
        return self._objects[formID]

    def objectsByName(self, name: str) -> List[Object]:
        """Retourne la liste des objects ayant le nom donné"""
        return [obj for obj in self._objects.values() if obj.name() == name]

    def minimalExport(self) -> dict:
        """Exporte uniquement les données nécessaires à l'affichage du monde"""
        return {
            "currentGroup": self._currentGroup,
            "currentIndex": self._currentIndex,
            "objects": [obj.toMinimalDict() for obj in self._objects.values()],
        }

    def destroyAll(self) -> None:
        """Détruit tous les objects"""
        for obj in self._objects.values():
            obj.destroy()

    def minimalImport(self, minimalExport: dict) -> None:
        """Charge le minimum de données nécessaires à l'affichage du monde.
        Attent un objet du même format qu'exporté par minimalExport()"""
        self._currentGroup = minimalExport["currentGroup"]
        self._currentIndex = minimalExport["currentIndex"]
        objs = [
            self.objectsClasses[obj["class"]](
                **self.objectsClasses[obj["class"]].fromMinimalDict(obj)
            )
            for obj in minimalExport["objects"]
        ]
        self._objects = {obj.formID(): obj for obj in objs}
        self._kartPlaceHolders = {
            obj.formID(): obj for obj in objs if isinstance(obj, Kart)
        }

    def finishLine(self) -> FinishLine:
        """Nom explicit"""
        return self._finishLine

    def clean(self, elapsedTime: float) -> None:
        """A appeler à la fin de chaque frame, supprime les objets devenus inutiles ou obsolètes"""
        for obj in [o for o in self._objects.values() if o.lastFrame()]:
            if isinstance(obj, Kart):
                self._kartPlaceHolders[obj.formID()] = obj
                obj.restore()

            self._destroyedObjects[obj.formID()] = obj
            self._objects.pop(obj.formID())


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
