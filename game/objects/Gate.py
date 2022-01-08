from typing import List

import lib

from .Polygon import Object, Polygon


class Gate(Polygon):
    def __init__(self, **kwargs) -> None:
        kwargs["isSolid"] = False
        super().__init__(**kwargs)
