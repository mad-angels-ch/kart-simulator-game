from typing import List, Tuple

from .Point import Point
from .Vector import Vector
from .Segment import Segment
from .Shape import Shape
from .Rectangle import Rectangle


class AlignedRectangle(Rectangle):
    _width: float
    _height: float
    _center: Point

    def __init__(
        self,
        width: float,
        height: float,
        leftBottom: Point = None,
        center: Point = None,
    ) -> None:
        if not leftBottom:
            if center:
                center.translate((-width / 2, -height / 2))
                leftBottom = center
            else:
                raise ValueError("Neither leftBottom or center has been given")
        super().__init__(
            leftBottom,
            Point((leftBottom.x() + width, leftBottom.y())),
            Point((leftBottom.x() + width, leftBottom.y() + height)),
        )

    def collides(self, other: Shape) -> bool:
        if isinstance(other, AlignedRectangle):

            def areOverlapping(
                alignedRectangles: List[AlignedRectangle], dimension: int
            ):
                def getMinMax(
                    alignedRectangle: AlignedRectangle, dimension: int
                ) -> Tuple[float, float]:
                    coordinates = [
                        alignedRectangle.vertex(i)[dimension] for i in [0, 2]
                    ]
                    return min(coordinates), max(coordinates)

                minMaxes = [
                    getMinMax(alignedRectangles[i], dimension) for i in range(2)
                ]
                if minMaxes[1][0] <= minMaxes[0][1] and minMaxes[0][0] <= minMaxes[1][1]:
                    return True
                else:
                    return False

            for i in range(2):
                if not areOverlapping([self, other], i):
                    return False
            return True

        else:
            return super().collides(other)
