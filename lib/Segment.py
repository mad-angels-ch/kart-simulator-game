from .vector import Vector
from .point import Point
from .Line import Line


class Segment(Line):
    def __init__(self, begin: Point, vectorOrEnd: "Vector | Point") -> None:
        super().__init__(begin, vectorOrEnd)

    def begin(self) -> Point:
        """Retourne une extrémité du segment"""
        return self.point()

    def end(self) -> Point:
        """Retourne l'autre extrémité du segment"""
        return Point(self.point()).translate(self.vector())

    def length(self) -> float:
        """Retourne la longueur du segment"""
        return self.vector().norm()

    def passBy(self, point: Point) -> bool:
        """Retourne True si le point donné en paramètre se trouve sur le segment"""
        vector = Vector.fromPoints(self._point, point)
        if not super().passBy(point):
            return False

        begin = self.begin()
        end = self.end()
        for i in range(len(point)):
            if min(begin[i], end[i]) > point[i] or max(begin[i], end[i]) < point[i]:
                return False

        return True
