from lib import Point


class Object:
    _name: str = None
    _formID: int

    _center: Point
    _angle: float

    def formID(self) -> int:
        return self._formID

    def name(self) -> str:
        return self._name

    def center(self) -> Point:
        return self._center

    def angle(self) -> float:
        return self._angle
