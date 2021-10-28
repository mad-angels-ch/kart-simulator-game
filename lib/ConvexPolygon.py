from typing import List

from .point import Point
from .vector import Vector
from .Line import Line
from .Segment import Segment
from .Polygon import Polygon


class ConvexPolygon(Polygon):
    def __init__(self, *vertices: Point) -> None:
        super().__init__(*vertices)

    def edgesNeededForSAT(self) -> List[Segment]:
        """Retourne le nombre minimal de côtés sur lesquels les projections sont nécessaires à SAT"""
        return self.edges()

    def separatingAxisTheorem(self, otherPolygon: "ConvexPolygon") -> bool:
        """Utilise Separating Axis Theorem (SAT) pour déterminer si les deux polygones convexes se collisionnent"""
        for edge in self.edgesNeededForSAT() + otherPolygon.edgesNeededForSAT():
            axis = Vector(*edge.vector())
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
