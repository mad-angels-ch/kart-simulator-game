import lib

from .VectorialMotion import VectorialMotion
from .UniformlyAcceleratedMotion import UniformlyAcceleratedMotion


class VectorialMotionFactory:
    """Factory function pour les mouvements linéaire, ne pas utiliser leurs constructeurs"""
    def __call__(self, type: str, **kwargs) -> VectorialMotion:
        if type == "none":
            vectorialMotion = VectorialMotion()
        elif type == "uam":
            vectorialMotion = self._uniformlyAcceleratedMotion(**kwargs)
        else:
            raise ValueError(f"{type} is not a valid type!")

        return vectorialMotion

    def _uniformlyAcceleratedMotion(self, **kwargs) -> UniformlyAcceleratedMotion:
        initialSpeed = kwargs.get("initialSpeed", lib.Vector((0, 0)))
        acceleration = kwargs.get("acceleration", lib.Vector((0, 0)))

        return UniformlyAcceleratedMotion(initialSpeed, acceleration)

    def fromFabric(self, jsonObject) -> VectorialMotion:
        """Créé et retourne à partir du format utilisé dans les jsons donnés le mouvement linéaire correspondant."""
        type = jsonObject["type"]
        kwargs = {}
        if type in ["uam"]:
            kwargs["initialSpeed"] = lib.Vector(list(jsonObject["velocity"].values()))
            kwargs["acceleration"] = lib.Vector(list(jsonObject["acceleration"].values()))

        return self.__call__(type=type, **kwargs)


createVectorialMotion = VectorialMotionFactory()
