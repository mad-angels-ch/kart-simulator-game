import lib

from .VectorialMotion import VectorialMotion
from .UniformlyAcceleratedMotion import UniformlyAcceleratedMotion
from .VectorialHarmonicMotion import VectorialHarmonicMotion

class VectorialMotionFactory:
    """Factory function pour les mouvements linéaire, ne pas utiliser leurs constructeurs"""
    def __call__(self, type: str, **kwargs) -> VectorialMotion:
        if type == "none":
            vectorialMotion = VectorialMotion()
        elif type == "uam":
            vectorialMotion = self._uniformlyAcceleratedMotion(**kwargs)
        elif type == "vhm":
            vectorialMotion = self._vectorialHarmonicMotion(**kwargs)
        else:
            raise ValueError(f"{type} is not a valid type!")

        return vectorialMotion

    def _uniformlyAcceleratedMotion(self, **kwargs) -> UniformlyAcceleratedMotion:
        initialSpeed = kwargs.get("initialSpeed", lib.Vector((0, 0)))
        acceleration = kwargs.get("acceleration", lib.Vector((0, 0)))

        return UniformlyAcceleratedMotion(initialSpeed, acceleration)

    def _vectorialHarmonicMotion(
        self, **kwargs
    ) -> VectorialHarmonicMotion:
        amplitude = kwargs.get("amplitude", 0)
        phase = kwargs.get("phase", 0)
        period = kwargs.get("period", 0)

        return VectorialHarmonicMotion(amplitude=amplitude, phase=phase, period=period)

    
    def fromFabric(self, jsonObject) -> VectorialMotion:
        """Créé et retourne à partir du format utilisé dans les jsons donnés le mouvement linéaire correspondant."""
        type = jsonObject["type"]
        kwargs = {}
        if type in ["uam"]:
            kwargs["initialSpeed"] = lib.Vector(list(jsonObject["velocity"].values()))
            kwargs["acceleration"] = lib.Vector(list(jsonObject["acceleration"].values()))
        elif type in ["vhm"]:
            kwargs["amplitude"] = lib.Vector(list(jsonObject["amplitude"].values()))
            kwargs["phase"] = jsonObject["phase"]
            kwargs["period"] = jsonObject["period"]

        return self.__call__(type=type, **kwargs)


createVectorialMotion = VectorialMotionFactory()
