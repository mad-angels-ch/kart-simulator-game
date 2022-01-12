import math

from .Vector import Vector
from .Point import Point
from .Line import Line


class Segment(Line):
    """Pour les segments"""
    def __init__(self, begin: Point, vectorOrEnd: "Vector | Point") -> None:
        super().__init__(begin, vectorOrEnd)

    def copy(self) -> "Segment":
        """Retourne une copie"""
        return Segment(self.point().copy(), self.vector().copy())

    def begin(self) -> Point:
        """Retourne une extrémité du segment"""
        return self.point()

    def end(self) -> Point:
        """Retourne l'autre extrémité du segment"""
        endPoint = Point(self.point())
        endPoint.translate(self.vector())
        return endPoint

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
            smallest = min(begin[i], end[i])
            biggest = max(begin[i], end[i])
            if (
                smallest > point[i]
                # and not math.isclose(smallest, point[i], abs_tol=Segment.precision)
            ) or (
                biggest < point[i]
                # and not math.isclose(biggest, point[i], abs_tol=Segment.precision)
            ):
                return False

        return True

    def intercepts(self, other: "Segment") -> bool:
        """Retourne True si les deux segments se coupent"""
        coefficients = self._vectorCoefficientsToIntersectionPoint(other)
        if not coefficients:
            return False
        return (
            0 <= coefficients[0]
            and coefficients[0] <= 1
            and 0 <= coefficients[1]
            and coefficients[1] <= 1
        )

    def intersection(self, other: "Segment") -> "Point | None":
        """Retourne le point d'intersection entre les segments s'il existe"""
        coefficients = self._vectorCoefficientsToIntersectionPoint(other)
        if not coefficients:
            return
        elif (
            0 <= coefficients[0]
            and coefficients[0] <= 1
            and 0 <= coefficients[1]
            and coefficients[1] <= 1
        ):
            return
        else:
            return Point(
                *[
                    self.begin()[i] + coefficients[0] * self.vector()[i]
                    for i in range(len(self.begin()))
                ]
            )
