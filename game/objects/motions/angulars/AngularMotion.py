from lib.point import Point
from lib.vector import Vector


class AngularMotion:
    def updateReferences(self, deltaTime: float) -> None:
        pass

    def rotationCenter(self) -> Point:
        return Point(0, 0)

    def set_rotationCenter(self, point: Point) -> None:
        pass

    def relativeAngle(self, deltaTime: float = 0) -> float:
        return 0

    def speed(self, deltaTime: float = 0) -> float:
        return 0

    def speedAtPoint(self, point: Point, deltaTime: float = 0) -> Vector:
        normal = Vector.fromPoints(self.rotationCenter(), point)
        speed = Vector(0, self.speed(deltaTime) * normal.norm())
        speed.rotate(normal.direction())
        return speed