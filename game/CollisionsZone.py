from typing import List

from lib import Point, Vector

from . import objects


class CollisionsZone:
    timePrecision = 1e-5

    _timeInterval: float
    _objects: List[objects.Object]

    def __init__(self, timeInterval: float) -> None:
        super().__init__()
        self._timeInterval = timeInterval
        self._objects = list()

    def __iadd__(self, objectToAdd: objects.Object) -> None:
        self._objects.append(objectToAdd)
        return self

    def _solveFirst(self, timeInterval: float) -> List[objects.Object]:
        transformations = [
            (obj.relativeAngle(timeInterval), obj.relativePosition(timeInterval))
            for obj in self._objects
        ]
        for i in range(len(self._objects)):
            self._objects[i].rotate(transformations[i][0])
            self._objects[i].translate(transformations[i][1])

        for object in self._objects:
            object.updateReferences(self._timeInterval)
            object.set_fill("#000000")
            
        for first in range(len(self._objects) - 1):
            for second in range(first + 1, len(self._objects)):
                if self._objects[first].collides(self._objects[second]):
                    self._objects[first].set_fill("#ff0000")
                    self._objects[second].set_fill("#ff0000")
        

    def resolve(self) -> None:
        self._solveFirst(self._timeInterval)