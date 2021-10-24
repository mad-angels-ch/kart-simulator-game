from lib.vector import Vector

from .VectorialMotion import VectorialMotion


class UniformlyAcceleratedMotion(VectorialMotion):
    _acceleration: Vector

    def __init__(self, initialSpeed=Vector(0, 0), acceleration=Vector(0, 0)) -> None:
        super().__init__()
        self._speed = initialSpeed
        self._acceleration = acceleration

    def updateReferences(self, deltaTime: float) -> None:
        self._speed = self.speed(deltaTime)

    def relativePosition(self, deltaTime: float = 0) -> Vector:
        return self._acceleration * (deltaTime ** 2 / 2) + self._speed * deltaTime

    def speed(self, deltaTime: float = 0) -> Vector:
        return self._acceleration * deltaTime + self._speed
