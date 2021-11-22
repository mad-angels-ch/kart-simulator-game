from logging import warning
import math

import lib


class AngularMotion:
    precision = 1e-6

    _speed: float
    _center: lib.Point
    _static: bool

    def __init__(self, speed: float = 0, center=lib.Point((0, 0))) -> None:
        self._speed = speed
        self._center = center
        self.updateIsStatic()

    def updateReferences(self, deltaTime: float) -> None:
        pass

    def center(self) -> lib.Point:
        return self._center

    def set_center(self, newCenter: lib.Point) -> None:
        self._center = newCenter

    def relativeAngle(self, deltaTime: float = 0) -> float:
        return self._speed * deltaTime

    def speed(self, deltaTime: float = 0) -> float:
        return self._speed

    def set_speed(self, newSpeed: float) -> None:
        self._speed = newSpeed
        self.updateIsStatic()

    def acceleration(self, deltaTime: float = 0) -> float:
        return 0

    def updateIsStatic(self) -> None:
        self._static = math.isclose(
            self.speed(), 0, abs_tol=self.precision
        ) and math.isclose(self.acceleration(), 0, abs_tol=self.precision)

    def isStatic(self) -> bool:
        return self._static

    def speedAtPoint(self, point: lib.Point, deltaTime: float = 0) -> lib.Vector:
        normal = lib.Vector.fromPoints(self.center(), point)
        speed = lib.Vector((0, self.speed(deltaTime) * normal.norm()))
        speed.rotate(normal.direction())
        return speed

    def accelerationAtPoint(self, point: lib.Point, deltaTime: float = 0) -> lib.Vector:
        normal = lib.Vector.fromPoints(self.center(), point)
        acceleration = lib.Vector((0, self.acceleration(deltaTime) * normal.norm()))
        acceleration.rotate(normal.direction())
        return acceleration
