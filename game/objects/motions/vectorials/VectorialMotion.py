import lib


class VectorialMotion:
    _speed: lib.Vector

    def __init__(self, speed: lib.Vector = lib.Vector()) -> None:
        self._speed = speed

    def updateReferences(self, deltaTime: float) -> None:
        pass

    def relativePosition(self, deltaTime: float = 0) -> lib.Vector:
        return self._speed * deltaTime

    def speed(self, deltaTime: float = 0) -> lib.Vector:
        return self._speed

    def set_speed(self, newSpeed: lib.Vector) -> None:
        self._speed = newSpeed

    def acceleration(self, deltaTime: float = 0) -> lib.Vector:
        return lib.Vector()
