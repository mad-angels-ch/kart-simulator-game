from lib.vector import Vector

class VectorialMotion:
    def updateReferences(self, deltaTime: float) -> None:
        pass

    def relativePosition(self, deltaTime: float = 0) -> Vector:
        return Vector(0, 0)

    def speed(self, deltaTime: float = 0) -> Vector:
        return Vector(0, 0)