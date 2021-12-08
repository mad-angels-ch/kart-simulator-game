from typing import List, Tuple

from .Point import Point
from .Vector import Vector
from .Segment import Segment
from .Shape import Shape
from .Rectangle import Rectangle


class AlignedRectangle(Rectangle):
    _width: float
    _height: float
    _leftBottom: Point

    def smallestContaining(*rectangles: "AlignedRectangle") -> "AlignedRectangle":
        """Retourne le plus petit rectangle contenant tous les rectangles donnés en paramètre."""
        container = rectangles[0]
        for rectangle in rectangles[1:]:
            container.set_left(min(container.left(), rectangle.left()))
            container.set_right(max(container.right(), rectangle.right()))
            container.set_bottom(min(container.bottom(), rectangle.bottom()))
            container.set_top(max(container.top(), rectangle.top()))
        return rectangle

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
        self._width = width
        self._height = height
        self._leftBottom = Point(leftBottom)

    def width(self) -> float:
        """Retourne la largeur du rectangle"""
        return self._width

    def height(self) -> float:
        """Retourne la hauteur du rectangle"""
        return self._height

    def leftBottom(self) -> Point:
        """NE PAS MODIFIER!
        Retourne le point inférieur gauche du rectangle."""
        return self._leftBottom

    def center(self) -> Point:
        """Retourne le centre du rectangle"""
        center = Point(self._leftBottom)
        center.translate(Vector((self._width / 2, self._height / 2)))
        return center

    def left(self) -> float:
        """Retourne la position la plus à gauche du rectangle."""
        return self._leftBottom.x()

    def set_left(self, newLeft: float) -> None:
        """Modifie la position la plus à gauche du rectangle."""
        self._leftBottom[0] = newLeft

    def right(self) -> float:
        """Retourne la position la plus à droite du rectangle."""
        return self.left() + self._width

    def set_right(self, newRight: float) -> None:
        """Modifie la position la plus à droite du rectangle."""
        self._width += newRight - self.right()

    def bottom(self) -> float:
        """Retourne la position la plus basse du rectangle."""
        return self._leftBottom.y()

    def set_bottom(self, newBottom: float) -> None:
        """Modifie la position la plus basse du rectangle."""
        self._leftBottom[1] = newBottom

    def top(self) -> float:
        """Retourne la position la plus haute du rectangle."""
        return self.bottom() + self._height

    def set_top(self, newTop: float) -> None:
        """Modifie la position la plus haute du rectangle."""
        self._height += newTop - self.top()

    def vertex(self, vertexIndex: int) -> Point:
        x = self.leftBottom().x()
        if vertexIndex in [1, 2]:
            x += self.width()
        y = self.leftBottom().y()
        if vertexIndex in [2, 3]:
            y += self.height()
        return Point((x, y))

    def vertices(self) -> List[Point]:
        return [self.vertex(i) for i in range(0, 4)]

    def resizeToInclude(self, other: "AlignedRectangle") -> None:
        """Agrandi le rectangle (si nécessaire) de manière à ce que l'autre rectangle (donné en paramètre) soint entièrement à l'intérieur"""
        self.set_left(min(self.left(), other.left()))
        self.set_right(max(self.right(), other.right()))
        self.set_bottom(min(self.bottom(), other.bottom()))
        self.set_top(max(self.top(), other.top()))

    def collides(self, other: Shape) -> bool:
        if isinstance(other, AlignedRectangle):
            return not (
                self.right() < other.left()
                or other.right() < self.left()
                or self.top() < other.bottom()
                or other.top() < self.bottom()
            )

        else:
            return super().collides(other)
