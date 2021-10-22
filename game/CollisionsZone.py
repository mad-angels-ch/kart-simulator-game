from typing import List
from lib import Point, Vector

from . import objects


class CollisionsZone:
    _objects: List[objects.Object] = list()

    def __iadd__(self, object: objects.Object) -> None:
        self._objects.append(object)
        return self

    def run(self, timeInterval: float) -> None:
        print(timeInterval)
        for object in self._objects:
            object.updateReferences(timeInterval)
            object.set_fill("#000000")
            
        for i in range(len(self._objects) - 1):
            for ii in range(i + 1, len(self._objects)):
                if self._objects[i].collides(self._objects[ii]):
                    self._objects[ii].set_fill("#ff0000")
                    self._objects[ii].set_fill("#ff0000")