from typing import List, Tuple
import os
import time

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

    def _solveFirst(self, timeInterval: float) -> float:
        # recherche du moment de la collision
        checkedInterval = 0
        halfWorkingInterval = timeInterval
        while halfWorkingInterval > self.timePrecision:
            transformations = [
                (
                    ob.relativeAngle(halfWorkingInterval),
                    ob.relativePosition(halfWorkingInterval),
                )
                for ob in self._objects
            ]
            for i in range(len(self._objects)):
                self._objects[i].rotate(transformations[i][0])
                self._objects[i].translate(transformations[i][1])

            def getCollidedObjects(objects: List[objects.Object]):
                for first in range(len(objects) - 1):
                    for second in range(first + 1, len(objects)):
                        if objects[first].collides(objects[second]):
                            return (objects[first], objects[second])
                return None

            collidedObjects = getCollidedObjects(self._objects)

            if collidedObjects:
                for i in range(len(self._objects)):
                    self._objects[i].rotate(-transformations[i][0])
                    self._objects[i].translate(-transformations[i][1])
                halfWorkingInterval /= 2
            else:
                if halfWorkingInterval == timeInterval:
                    # il n'y a aucune collision dans l'intervalle donnée à la fonction
                    return timeInterval
                checkedInterval += halfWorkingInterval
                halfWorkingInterval /= 2

        # gestion de la collision
        pass

    def resolve(self) -> None:
        self._solveFirst(self._timeInterval)
