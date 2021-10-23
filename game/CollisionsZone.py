from logging import info
from typing import List, Callable, Any, Iterable, Mapping
from threading import Thread
from multiprocessing import Process
import time


from lib import Point, Vector

from . import objects


class CollisionsZone:
    _timeInterval: float
    _objects: List[objects.Object]

    def __init__(self, timeInterval: float) -> None:
        self._timeInterval = timeInterval
        self._objects = list()

    def __iadd__(self, objectToAdd: objects.Object) -> None:
        self._objects.append(objectToAdd)
        return self

    def run(self) -> None:
        for object in self._objects:
            object.updateReferences(self._timeInterval)
            object.set_fill("#000000")

        for first in range(len(self._objects) - 1):
            for second in range(first + 1, len(self._objects)):
                if self._objects[first].collides(self._objects[second]):
                    self._objects[first].set_fill("#ff0000")
                    self._objects[second].set_fill("#ff0000")