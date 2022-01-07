import math
import lib


class VectorialMotion:
    _speed: lib.Vector
    _static: bool

    def __init__(self, speed: lib.Vector = lib.Vector()) -> None:
        self._speed = speed
        self.updateIsStatic()

    def updateReferences(self, deltaTime: float) -> None:
        pass

    def relativePosition(self, deltaTime: float = 0) -> lib.Vector:
        return self._speed * deltaTime

    def speed(self, deltaTime: float = 0) -> lib.Vector:
        return self._speed

    def set_speed(self, newSpeed: lib.Vector) -> None:
        self._speed = newSpeed
        self.updateIsStatic()

    def acceleration(self, deltaTime: float = 0) -> lib.Vector:
        return lib.Vector()

    def set_acceleration(self, newAcceleration: lib.Vector) -> None:
        raise RuntimeError("You can't change the vectorial acceleration of this object")

    def updateIsStatic(self) -> None:
        self._static = self._speed == lib.Vector()

    def isStatic(self) -> bool:
        return self._static
