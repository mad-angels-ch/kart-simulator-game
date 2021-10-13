from lib import Point, Vector

from . import motions


class Object:
    _name: str = None
    _formID: int

    _center: Point
    _angle: float

    angularMotion: motions.angulars.AngularMotion
    vectorialMotion: motions.vectorials.VectorialMotion

    _fill: str
    _opacity: float

    def formID(self) -> int:
        return self._formID

    def name(self) -> str:
        return self._name

    def center(self) -> Point:
        return self._center

    def angle(self) -> float:
        return self._angle

    def fill(self) -> str:
        return self._fill

    def opacity(self) -> float:
        return self._opacity

    # def translate(self, vector: Vector) -> None:
    #     self.center.