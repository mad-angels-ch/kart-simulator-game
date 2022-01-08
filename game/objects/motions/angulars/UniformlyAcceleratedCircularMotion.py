import lib

from .AngularMotion import AngularMotion


class UniformlyAcceleratedCircularMotion(AngularMotion):
    _acceleration: float

    def __init__(
        self,
        rotationCenter: lib.Point = lib.Point((0, 0)),
        initialSpeed: float = 0,
        acceleration: float = 0,
    ) -> None:
        self._acceleration = acceleration
        super().__init__(initialSpeed, rotationCenter)

    def updateIsStatic(self) -> None:
        self._static = not self._speed and not self._acceleration

    def updateReferences(self, deltaTime: float) -> None:
        self._speed = self.speed(deltaTime)
        self.updateIsStatic()

    def relativeAngle(self, deltaTime: float = 0) -> float:
        return self._acceleration * (deltaTime ** 2 / 2) + self._speed * deltaTime

    def speed(self, deltaTime: float = 0) -> float:
        return self._acceleration * deltaTime + self._speed

    def acceleration(self, deltaTime: float = 0) -> float:
        return self._acceleration

    def set_acceleration(self, newAcceleration: float) -> None:
        self._acceleration = newAcceleration
