from lib.point import Point

from .AngularMotion import AngularMotion


class UniformlyAcceleratedCircularMotion(AngularMotion):
    _center: Point
    _speed: float
    _acceleration: float

    def __init__(
        self,
        rotationCenter=Point(0, 0),
        initialSpeed: float = 0,
        acceleration: float = 0,
    ) -> None:
        super(UniformlyAcceleratedCircularMotion, self).__init__()
        self._center = rotationCenter
        self._speed = initialSpeed
        self._acceleration = acceleration

    def updateReferences(self, deltaTime: float) -> None:
        self._speed = self.speed(deltaTime)

    def rotationCenter(self) -> Point:
        return self._center

    def relativeAngle(self, deltaTime: float = 0) -> float:
        return self._acceleration * (deltaTime ** 2 / 2) + self._speed * deltaTime

    def speed(self, deltaTime: float = 0) -> float:
        return self._acceleration * deltaTime + self._speed
