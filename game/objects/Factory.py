from typing import Dict, List
from math import radians

import lib

from .Object import Object
from .Circle import Circle
from .Polygon import Polygon
from . import motions


class Factory:
    objectsCreatedCount = 0

    def __call__(
        self,
        type: str,
        name: str = None,
        center: lib.Point = lib.Point((0, 0)),
        angle: float = 0,
        angularMotion=motions.angulars.AngularMotion(),
        vectorialMotion=motions.vectorials.VectorialMotion(),
        fill="#000000",
        opacity: float = 1,
        mass=0,
        friction=0,
        **kwargs,
    ) -> Object:
        if type == "circle":
            newObject = self._circleBefore(**kwargs)
        elif type == "polygon":
            newObject = self._polygonBefore(**kwargs)
        else:
            raise ValueError(f"{type} is not a valid type!")

        newObject._name = name
        newObject._formID = Factory.objectsCreatedCount
        newObject._center = center
        newObject._angle = angle
        newObject.angularMotion = angularMotion
        newObject.vectorialMotion = vectorialMotion
        newObject._opacity = opacity
        newObject._mass = mass
        newObject._friction = friction

        if fill[0] != '#':      # Transformation des couleurs rgb en hex
            f = fill[4:-1].split(',')
            l = list()
            for i in f:
                l.append(int(i))
            newObject._fill = '#%02x%02x%02x' % (l[0],l[1],l[2])
        else:
            newObject._fill = fill
            
        if type == "circle":
            self._circleAfter(newObject, **kwargs)
        elif type == "polygon":
            self._polygonAfter(newObject, **kwargs)
        else:
            raise ValueError(f"{type} is not a valid type!")

        Factory.objectsCreatedCount += 1
        return newObject

    def _circleBefore(self, **kwargs):
        newObject = Circle()
        return newObject

    def _circleAfter(self, newObject: Circle, **kwargs):
        newObject._radius = kwargs.get("radius", 0)

    def _polygonBefore(self, **kwargs):
        newObject = Polygon()
        return newObject

    def _polygonAfter(self, newObject: Polygon, **kwargs):
        newObject._vertices = kwargs.get("vertices", [])
        newObject.updateAngleCosSin()

    def fromFabric(self, jsonObject) -> List[Object]:
        objects = []
        if jsonObject.get("version") == "4.4.0":
            for fabricObject in jsonObject.get("objects"):
                type = fabricObject["type"]
                name = fabricObject["lge"].get("name")
                center = lib.Point((fabricObject["left"], fabricObject["top"]))
                angle = radians(fabricObject["angle"])
                fill = fabricObject["fill"]
                opacity = fabricObject["opacity"]

                friction = fabricObject["lge"]["friction"]
                mass = fabricObject["lge"]["mass"]
                angularMotion = motions.angulars.createAngularMotion.fromFabric(
                    fabricObject["lge"]["motion"]["angle"]
                )
                vectorialMotion = motions.vectorials.createVectorialMotion.fromFabric(
                    fabricObject["lge"]["motion"]["vector"]
                )

                scaleX, scaleY = fabricObject["scaleX"], fabricObject["scaleY"]
                if fabricObject["flipX"]:
                    scaleX *= -1
                if fabricObject["flipY"]:
                    scaleY *= -1

                kwargs = {}
                if type == "circle":
                    kwargs["radius"] = fabricObject["radius"] * scaleX

                elif type == "polygon":
                    kwargs["vertices"] = [
                        lib.Point(list(point.values())) for point in fabricObject["points"]
                    ]
                    abscissas = [point[0] for point in kwargs["vertices"]]
                    ordinates = [point[1] for point in kwargs["vertices"]]

                    toOrigin = -lib.Vector((
                        (min(abscissas) + max(abscissas)) / 2,
                        (min(ordinates) + max(ordinates)) / 2,
                    ))

                    for i in range(len(kwargs["vertices"])):
                        kwargs["vertices"][i].translate(toOrigin)
                        pointV = lib.Vector(kwargs["vertices"][i])

                        pointV.scaleX(scaleX)
                        pointV.scaleY(scaleY)

                        kwargs["vertices"][i] = lib.Point(pointV)

                objects.append(
                    self.__call__(
                        type=type,
                        name=name,
                        center=center,
                        angle=angle,
                        angularMotion=angularMotion,
                        vectorialMotion=vectorialMotion,
                        fill=fill,
                        opacity=opacity,
                        mass=mass,
                        friction=friction,
                        **kwargs,
                    )
                )

        return objects


create = Factory()
