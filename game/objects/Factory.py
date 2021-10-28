from typing import Dict, List
from math import radians

from lib import Point, Vector

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
        center: Point = Point(0, 0),
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
        newObject._fill = fill
        newObject._opacity = opacity
        newObject._mass = mass
        newObject._friction = friction

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
        newObject._summits = kwargs.get("summits", [])
        newObject.updateAngleCosSin()

    def fromFabric(self, jsonObject) -> List[Object]:
        objects = []
        if jsonObject.get("version") == "4.4.0":
            for fabricObject in jsonObject.get("objects"):
                type = fabricObject["type"]
                name = fabricObject["lge"].get("name")
                center = Point(fabricObject["left"], fabricObject["top"])
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
                    kwargs["summits"] = [
                        Point(*point.values()) for point in fabricObject["points"]
                    ]
                    abscissas = [point["x"] for point in kwargs["summits"]]
                    ordinates = [point["y"] for point in kwargs["summits"]]

                    toOrigin = -Vector(
                        (min(abscissas) + max(abscissas)) / 2,
                        (min(ordinates) + max(ordinates)) / 2,
                    )

                    for point in kwargs["summits"]:
                        point.translate(toOrigin)
                        pointV = Vector(*point)

                        pointV.scaleX(scaleX)
                        pointV.scaleY(scaleY)
                        pointV.rotate(angle)

                        point = Point(*center)
                        point.translate(pointV)

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
