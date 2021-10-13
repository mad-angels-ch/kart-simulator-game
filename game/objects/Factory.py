from typing import Dict, List

from lib.point import Point

from .Object import Object
from .Circle import Circle
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
        **kwargs,
    ) -> Object:
        if type == "circle":
            newObject = self._circle(**kwargs)
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

        Factory.objectsCreatedCount += 1
        return newObject

    def _circle(self, **kwargs):
        newObject = Circle()

        newObject._radius = kwargs.get("radius", 0)

        return newObject

    def fromFabric(self, jsonObject) -> List[Object]:
        objects = []
        if jsonObject.get("version") == "4.4.0":
            for fabricObject in jsonObject.get("objects"):
                type = fabricObject["type"]
                name = fabricObject["lge"].get("name")
                center = Point(fabricObject["left"], fabricObject["top"])
                angle = fabricObject["angle"]
                fill = fabricObject["fill"]

                friction = fabricObject["lge"]["friction"]
                mass = fabricObject["mass"]["mass"]
                angularMotion = motions.angulars.createAngularMotion.fromFabric(
                    fabricObject["lge"]["motion"]["angle"]
                )

                scaleX, scaleY = fabricObject["scaleX"], fabricObject["scaleY"]
                flipX, flipY = fabricObject["flipX"], fabricObject["flipY"]

                kwargs = {}
                if type == "circle":
                    kwargs["radius"] = fabricObject["radius"] * scaleX

                objects.append(self.__call__(type, name, center, angle, fill, **kwargs))

        return objects


create = Factory()
