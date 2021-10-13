from .Object import Object


class Circle(Object):
    _radius: float = 0

    def radius(self) -> float:
        return self._radius