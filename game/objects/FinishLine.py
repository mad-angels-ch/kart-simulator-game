import lib

from .Polygon import Object, Polygon

class FinishLine(Polygon):
    _originalVertices: list[float]
    def __init__(self, **kwargs) -> None:
        super().__init__(**kwargs)
        