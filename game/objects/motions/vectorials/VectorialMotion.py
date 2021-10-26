from lib.vector import Vector


class VectorialMotion:
    _speed: Vector

    def __init__(self, speed: Vector = Vector(0, 0)) -> None:
        self._speed = speed

    def updateReferences(self, deltaTime: float) -> None:
        pass

    def relativePosition(self, deltaTime: float = 0) -> Vector:
        return self._speed * deltaTime

    def speed(self, deltaTime: float = 0) -> Vector:
        return self._speed

    def set_speed(self, newSpeed: Vector) -> None:
        self._speed = newSpeed
