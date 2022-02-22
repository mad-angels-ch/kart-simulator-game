import lib

from .HarmonicMotion import HarmonicMotion
from .UniformlyAcceleratedHarmonicMotion import UniformlyAcceleratedHarmonicMotion


class HarmonicMotionFactory:
    """Factory function pour les mouvements harmoniques, ne pas utiliser leurs constructeurs"""

    def __call__(self, type: str, **kwargs) -> HarmonicMotion:
        """Créé et retourne à partir des argments donnés le mouvement angulaire correspondant."""
        if type == "none":
            harmonicMotion = HarmonicMotion()
        elif type == "hm":
            harmonicMotion = self._harmonicMotion(**kwargs)
        else:
            raise ValueError(f"{type} is not a valid type!")

        return harmonicMotion

    # def _uniformlyAcceleratedHarmonicMotion(
    #     self, **kwargs
    # ) -> UniformlyAcceleratedHarmonicMotion:
    #     center = kwargs.get("center", lib.Point((0, 0)))
    #     amplitude = kwargs.get("amplitude", 0)
    #     phase = kwargs.get("phase", 0)
    #     angularFrequency = kwargs.get("angularFrequency", 0)

    #     return UniformlyAcceleratedHarmonicMotion(center, amplitude, phase, angularFrequency)
    
    def _harmonicMotion(
        self, **kwargs
    ) -> HarmonicMotion:
        center = kwargs.get("center", lib.Point((0, 0)))
        amplitude = kwargs.get("amplitude", 0)
        phase = kwargs.get("phase", 0)
        angularFrequency = kwargs.get("angularFrequency", 0)

        return HarmonicMotion(center=center, amplitude=amplitude, phase=phase, angularFrequency=angularFrequency)

    def fromFabric(self, jsonObject) -> HarmonicMotion:
        """Créé et retourne à partir du format utilisé dans les jsons donnés le mouvement harmonique correspondant."""
        type = jsonObject["type"]
        kwargs = {}
        if type in ["uahm"]:
            kwargs["center"] = lib.Point(
                (float(jsonObject["center"]["x"]), float(jsonObject["center"]["y"]))
            )
            kwargs["amplitude"] = jsonObject["amplitude"]
            kwargs["phase"] = jsonObject["phase"]
            kwargs["angularFrequency"] = jsonObject["angularFrequency"]

        return self.__call__(type=type, **kwargs)


createHarmonicMotion = HarmonicMotionFactory()
