from lib import Point, Vector

from .Object import Object


class Circle(Object):
    _radius: float

    def __init__(self) -> None:
        super().__init__()
        self._radius = 0

    def radius(self) -> float:
        return self._radius

    def collides(self, object: "Object") -> bool:
        if isinstance(object, Circle):
            return (
                self.center().distanceOf(object.center())
                < self.radius() + object.radius()
            )

        else:
            return object.collides(self)

    def collisionPoint(self, object: "Object") -> Point:
        if isinstance(object, Circle):
            collisionPoint = Point(self.center())
            collisionPoint.translate(
                Vector.fromPoints(self.center(), object.center()).set_norm(
                    self.radius()
                )
            )
            return collisionPoint

        else:
            return object.collisionPoint(self)

    def collisionTangent(self, object: "Object") -> Vector:
        if isinstance(object, Circle):
            return Vector.fromPoints(self.center(), object.center()).normalVector()

        else:
            return object.collisionTangent(self)
