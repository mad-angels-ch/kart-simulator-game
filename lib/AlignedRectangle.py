from .Point import Point
from .Vector import Vector


class AlignedRectangle:
    _width: float
    _height: float
    _center: Point

    def __init__(
        self,
        width: float,
        height: float,
        center: Point = None,
        bottomLeft: Point = None,
    ) -> None:
        self._width = width
        self._height = height
        if center:
            self._center = center
        elif bottomLeft:
            self._center = bottomLeft.translate(self._width / 2, self._height / 2)
        else:
            raise ValueError("Neither center or bottomLeft has been given")
