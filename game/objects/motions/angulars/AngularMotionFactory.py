from lib import Point, Vector

from .AngularMotion import AngularMotion
from .UniformlyAcceleratedCircularMotion import UniformlyAcceleratedCircularMotion


class AngularMotionFactory:
    def __call__(self, type: str, **kwargs) -> AngularMotion:
        if type == "none":
            angularMotion = AngularMotion()
        elif type == "uacm":
            angularMotion = self._uniformlyAcceleratedCircularMotion(**kwargs)
        else:
            raise ValueError(f"{type} is not a valid type!")

        return angularMotion

    def _uniformlyAcceleratedCircularMotion(
        self, **kwargs
    ) -> UniformlyAcceleratedCircularMotion:
        center = kwargs.get("center", Point(0, 0))
        initialSpeed = kwargs.get("initialSpeed", 0)

        return UniformlyAcceleratedCircularMotion(center, initialSpeed)

    def fromFabric(self, jsonObject) -> AngularMotion:
        type = jsonObject["type"]
        kwargs = {}
        if type in ["uacm"]:
            kwargs["center"] = Point(*jsonObject["center"])
            kwargs["initialSpeed"] = jsonObject["velocity"]

        return self.__call__(type=type, **kwargs)


createAngularMotion = AngularMotionFactory()
