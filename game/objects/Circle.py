from .Object import Object


class Circle(Object):
    _radius: float = 0

    def radius(self) -> float:
        return self._radius

    def collides(self, object: "Object") -> bool:
        if isinstance(object, Circle):
            if self.center().distanceOf(object.center()) < self.radius() + object.radius():
                self._fill = "#ff0000"
                object._fill = "#ff0000"
                return True
            else:
                return False
        else:
            return object.collides(self)