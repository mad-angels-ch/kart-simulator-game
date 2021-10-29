from typing import List
from math import inf

from .point import Point
from .vector import Vector
from .Line import Line
from .Segment import Segment
from .Shape import Shape
from .Circle import Circle
from .Polygon import Polygon


class ConvexPolygon(Polygon):
    def __init__(self, *vertices: Point) -> None:
        super().__init__(*vertices)

    def collides(self, other: Shape) -> bool:
        if isinstance(other, Circle):
            return self._separatingAxisTheoremCircle(other)

        elif isinstance(other, ConvexPolygon):
            return self._separatingAxisTheoremConvexPolygon(other)

        else:
            return other.collides(self)

    def _edgesNeededForSAT(self) -> List[Segment]:
        """Retourne le nombre minimal de côtés sur lesquels les projections sont nécessaires à SAT"""
        return self.edges()

    def _separatingAxisTheoremCircle(self, circle: Circle) -> bool:
        # trouver le sommet le plus proche du cercle
        minDistance = inf
        for vertex in self.vertices():
            relation = Vector.fromPoints(circle.center(), vertex)
            squareDistance = relation[0] ** 2 + relation[1] ** 2
            if squareDistance < minDistance:
                minDistance = squareDistance
                minRelation = relation

        # tester chaques axes
        for axis in [
            edge.vector().normalVector() for edge in self._edgesNeededForSAT()
        ] + [minRelation]:
            myProjections = [
                axis.scalarProduct(Vector(*vertex)) for vertex in self.vertices()
            ]
            hisProjection = axis.scalarProduct(Vector(*circle.center()))
            myMin, myMax = (fun(myProjections) for fun in (min, max))
            hisMin, hisMax = (
                hisProjection - circle.radius(),
                hisProjection + circle.radius(),
            )
            if myMin > hisMax or myMax < hisMin:
                return False

        return True

    def _separatingAxisTheoremConvexPolygon(
        self, otherPolygon: "ConvexPolygon"
    ) -> bool:
        """Utilise Separating Axis Theorem (SAT) pour déterminer si les deux polygones convexes se collisionnent"""
        for edge in self._edgesNeededForSAT() + otherPolygon._edgesNeededForSAT():
            axis = edge.vector().normalVector()
            myProjections = [
                axis.scalarProduct(Vector(*vertex)) for vertex in self.vertices()
            ]
            hisProjections = [
                axis.scalarProduct(Vector(*vertex))
                for vertex in otherPolygon.vertices()
            ]
            myMin, myMax = (fun(myProjections) for fun in (min, max))
            hisMin, hisMax = (fun(hisProjections) for fun in (min, max))
            if myMin > hisMax or myMax < hisMin:
                return False

        return True
