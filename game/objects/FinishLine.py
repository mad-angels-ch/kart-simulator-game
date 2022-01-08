from typing import List

import lib

from .Polygon import Object, Polygon

class FinishLine(Polygon):
    _originalVertices: List[float]
    def __init__(self, **kwargs) -> None:
        super().__init__(**kwargs)
        
