import math
import inspect
from logging import INFO, warning
from typing import List

import lib

from .Polygon import Polygon


class FinishLine(Polygon):
    
    collisions_history = dict()
    
    def __init__(self, **kwargs) -> None:
        super().__init__(**kwargs)
        self._fill = "repeatPattern"
        

    def collides(self, other: "Object", timeInterval: float) -> bool:
        if type(other).__name__ == "Kart":
            newSelf = lib.Polygon(*self.vertices(timeInterval))
            newOther = lib.Polygon(*other.vertices(timeInterval))
            if newSelf.collides(newOther):
                self.saveCollision(other)
                return True
        
        
        
    def saveCollision(self, other: "Object"):
        self.collisions_history[other.formID()]=self.collisions_history.get(other.formID(),0) + 1
        INFO("Object number {} just passed through the finishline".format(other.formID()))