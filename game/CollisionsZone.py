from logging import info
from typing import List, Tuple
import os
import time
import math

from lib import Point, Vector

from . import objects


class CollisionsZone:
    timePrecision = 1e-3

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
        # start = time.time()

        # recherche du moment de la collision
        checkedInterval = 0
        halfWorkingInterval = timeInterval
        lastCollidedObjects = None
        # i = 0
        # counts = {}
        while halfWorkingInterval > self.timePrecision:

            def getCollidedObjects(objects: List[objects.Object]):
                for first in range(len(objects) - 1):
                    for second in range(first + 1, len(objects)):
                        # start = time.time()
                        if objects[first].collides(
                            objects[second], halfWorkingInterval
                        ):
                            return (objects[first], objects[second])
                        # end = time.time() - start
                        # print(end)
                        # if end:
                        #     print(end, first, second)
                        #     counts[first] = counts.get(first, 0) + 1
                        #     counts[second] = counts.get(second, 0) + 1
                # theKey = -1
                # theValue = 0
                # for key, value in counts.items():
                #     if value > theValue:
                #         theValue = value
                #         theKey = key
                # print(theKey, theValue)
                return None

            collidedObjects = getCollidedObjects(self._objects)
            # i += 1
            # print(i)
            # print(time.time() - start)

            if collidedObjects:
                lastCollidedObjects = collidedObjects
            else:
                for obj in self._objects:
                    obj.updateReferences(timeInterval)
                if not lastCollidedObjects:
                    # il n'y a aucune collision dans l'intervalle donnée à la fonction
                    # print(time.time() - start)
                    return timeInterval
                checkedInterval += halfWorkingInterval
            halfWorkingInterval /= 2

        # gestion de la collision
        info("Collision")
        point, tangent = lastCollidedObjects[0].collisionPointAndTangent(
            lastCollidedObjects[1]
        )
        angle = tangent.direction()

        masses = [obj.mass() for obj in lastCollidedObjects]
        objSpeeds = [obj.vectorialMotion.speed() for obj in lastCollidedObjects]
        pointSpeeds = [obj.speedAtPoint(point) for obj in lastCollidedObjects]
        speedsBefore = objSpeeds.copy()
        speedsBefore.extend(pointSpeeds)
        for speed in speedsBefore:
            speed.rotate(-angle)
        speedsAfter = [Vector(speed) for speed in objSpeeds]

        other = len(masses) - 1
        for current in range(len(masses)):
            m1 = masses[current]
            m2 = masses[other]
            v1 = objSpeeds[current][1]
            v2 = pointSpeeds[other][1]

            if m1:
                if m2:
                    speedsAfter[current][1] = 2 * (m1 * v1 + m2 * v2) / (m1 + m2) - v1
                else:
                    speedsAfter[current][1] = 2 * v2 - v1
            else:
                if m2:
                    speedsAfter[current][1] = v1
                else:
                    raise "Collision between two fixed objects"

            other = current

        for current in range(len(masses)):
            speedsAfter[current].rotate(angle)
            speedsAfter[current] *= (1 - lastCollidedObjects[current].friction()) * (
                1 - lastCollidedObjects[other].friction()
            )
            lastCollidedObjects[current].vectorialMotion.set_speed(speedsAfter[current])

            other = current

        return checkedInterval

    def resolve(self) -> None:
        while self._timeInterval > 0:
            self._timeInterval -= self._solveFirst(self._timeInterval)
