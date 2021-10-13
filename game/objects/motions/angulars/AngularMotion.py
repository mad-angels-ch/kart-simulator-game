from lib.point import Point


class AngularMotion:
    def updateReferences(self, deltaTime: float) -> None:
        pass

    def rotationCenter(self) -> Point:
        return Point(0, 0)

    def relativeAngle(self, deltaTime: float = 0) -> float:
        return 0

    def speed(self, deltaTime: float = 0) -> float:
        return 0
