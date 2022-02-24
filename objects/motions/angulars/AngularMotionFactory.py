import lib

from .AngularMotion import AngularMotion
from .UniformlyAcceleratedCircularMotion import UniformlyAcceleratedCircularMotion
from .AngularHarmonicMotion import AngularHarmonicMotion


class AngularMotionFactory:
    """Factory function pour les mouvements angulaires, ne pas utiliser leurs constructeurs"""

    def __call__(self, type: str, **kwargs) -> AngularMotion:
        """Créé et retourne à partir des argments donnés le mouvement angulaire correspondant."""
        if type == "none":
            angularMotion = AngularMotion()
        elif type == "uacm":
            angularMotion = self._uniformlyAcceleratedCircularMotion(**kwargs)
        elif type == "ahm":
            angularMotion = self._angularHarmonicMotion(**kwargs)
        else:
            raise ValueError(f"{type} is not a valid type!")

        return angularMotion

    def _uniformlyAcceleratedCircularMotion(
        self, **kwargs
    ) -> UniformlyAcceleratedCircularMotion:
        center = kwargs.get("center", lib.Point())
        initialSpeed = kwargs.get("initialSpeed", 0)
        acceleration = kwargs.get("acceleration", 0)

        return UniformlyAcceleratedCircularMotion(center, initialSpeed, acceleration)

    def _angularHarmonicMotion(self, **kwargs) -> AngularHarmonicMotion:
        amplitude = kwargs.get("amplitude", 0)
        phase = kwargs.get("phase", 0)
        frequency = kwargs.get("frequency", 0)
        center = kwargs.get("center", lib.Point())

        return AngularHarmonicMotion(amplitude=amplitude, phase=phase, frequency=frequency, center=center)  
    
    def fromFabric(self, jsonObject) -> AngularMotion:
        """Créé et retourne à partir du format utilisé dans les jsons donnés le mouvement angulaire correspondant."""
        type = jsonObject["type"]
        kwargs = {}
        if type in ["uacm"]:
            kwargs["center"] = lib.Point(
                (float(jsonObject["center"]["x"]), float(jsonObject["center"]["y"]))
            )
            kwargs["initialSpeed"] = jsonObject["velocity"]
            kwargs["acceleration"] = jsonObject["acceleration"]
        elif type in ["ahm"]:
            kwargs["amplitude"] = jsonObject["amplitude"]
            kwargs["phase"] = jsonObject["phase"]
            kwargs["frequency"] = jsonObject["frequency"]
            kwargs["center"] = lib.Point(
                (float(jsonObject["center"]["x"]), float(jsonObject["center"]["y"]))
            )
        return self.__call__(type=type, **kwargs)


createAngularMotion = AngularMotionFactory()
