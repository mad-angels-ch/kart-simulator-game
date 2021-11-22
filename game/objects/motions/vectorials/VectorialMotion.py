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

    def updateIsStatic(self) -> None:
        if self._speed:
            self._static = False
        else:
            self._static = True

    def isStatic(self) -> bool:
        return self._static
