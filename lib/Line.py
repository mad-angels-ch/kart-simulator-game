import math

from .vector import Vector
from .point import Point


class Line:
    precision = 1e-6

    _point: Point
    _vector: Vector

    def __init__(self, point: Point, vectorOrSecondPoint: "Vector | Point") -> None:
        self._point = point
        if type(vectorOrSecondPoint) == Vector:
            self._vector = vectorOrSecondPoint
        elif type(vectorOrSecondPoint) == Point:
            self._vector = Vector.fromPoints(point, vectorOrSecondPoint)
        else:
            raise TypeError("vectorOrSecondPoint is neither a point nor a vector")

    def point(self) -> Point:
        """Retourne un point de la droite"""
        return self._point

    def vector(self) -> Vector:
        """Retourne un vecteur directeur de la droite"""
        return self._vector

    def normalVector(self) -> Vector:
        """Retourne un vecteur normal à la droite"""
        return self._vector.normalVector()

    def orthogonalProjection(self, pointOrVector: "Point | Vector") -> "Point | Vector":
        """Projete le vecteur ou le point donné en paramètre sur la droite"""
        if type(pointOrVector) == Point:
            vectorToProject = Vector.fromPoints(self.point(), pointOrVector)
        else:
            vectorToProject: Vector = pointOrVector

        projectedVector = vectorToProject.orthogonalProjection(self._vector)
        if type(pointOrVector) == Point:
            projectedPoint = Point(*self._point)
            projectedPoint.translate(projectedPoint)
            return projectedPoint
        else:
            return projectedVector

    def sameOrientation(self, vector: Vector) -> bool:
        """Retourne vrai si le vecteur donné en paramètre est collinéaire à la doitre"""
        self._vector.isCollinear(vector)

    def passBy(self, point: Point) -> bool:
        """Retourne True si le point donné en paramètre se trouve sur la droite"""
        return Vector.fromPoints(self._point, point).isCollinear(self._vector)

    def _vectorCoefficientToIntersectionPoint(self, other: "Line") -> "float | None":
        denominator = (
            self.vector()[0] * other.vector()[1] - self.vector()[1] * other.vector()[0]
        )
        if math.isclose(denominator, 0, abs_tol=Line.precision):
            return None

        otherEnd = Point(*other.point())
        otherEnd.translate(other.vector())
        return (
            (self.point()[0] - other.point()[0]) * (other.point()[1] - otherEnd[1])
            - (self.point()[1] - other.point()[1]) * (other.point()[0] - otherEnd[1])
        ) / denominator

    def intercepts(self, other: "Line") -> bool:
        """Retourne True si les deux droites se coupent"""
        return bool(self._vectorCoefficientToIntersectionPoint(other))

    def intersection(self, other: "Line") -> "Point | None":
        """Retourne le point d'intersection entre les droites s'il existe"""
        coefficient = self._vectorCoefficientToIntersectionPoint(other)
        if not coefficient:
            return
        else:
            return Point(
                *[
                    self.point()[i] + coefficient * self.vector()[i]
                    for i in range(self.point())
                ]
            )
