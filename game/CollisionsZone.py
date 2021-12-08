from logging import info
from typing import List, Tuple
import os
import time
import math
from game.objects.Object import Object

from lib import Point, Vector
import lib

from . import objects


class CollisionsZone:
    timePrecision = 1e-3

    def create(
        objectsList: List[objects.Object], timeInterval: float
    ) -> Tuple[List["CollisionsZone"], List[objects.Object]]:
        """Détermine et retourne les différentes zones où il peut potentiellement avoir des collisions
        entre les objects donnés dans l'intervalle de temps donné.
        Retourne aussi la liste des objets ne se trouvant dans aucune zone."""
        moving = [obj for obj in objectsList if not obj.isStatic()]
        static = [obj for obj in objectsList if obj.isStatic()]
        zones = []

        def moveCollidingToZone(
            zone: CollisionsZone, objs: List[objects.Object]
        ) -> None:
            for obj in objs:
                if zone.collides(obj):
                    zone += obj
                    objs.remove(obj)

        while moving:
            zones.append(CollisionsZone(timeInterval, moving.pop()))
            moveCollidingToZone(zones[-1], moving)
            moveCollidingToZone(zones[-1], static)

        return zones, moving + static

    _timeInterval: float
    _objects: List[objects.Object]
    _dimension: lib.AlignedRectangle

    def __init__(self, timeInterval: float, *objectsInside: objects.Object) -> None:
        super().__init__()
        self._timeInterval = timeInterval
        self._objects = list(objectsInside)
        self._dimension = lib.AlignedRectangle.smallestContaining(
            *[obj.potentialCollisionZone(timeInterval) for obj in objectsInside]
        )

    def collides(self, objectToCheck: objects.Object) -> bool:
        """Retourne vrai si l'objet donné en paramètre se trouve dans la zone."""
        return self._dimension.collides(objectToCheck.potentialCollisionZone(self._timeInterval))

    def __iadd__(self, objectToAdd: objects.Object) -> None:
        """Ajoute un objet à la zone et redimensionne celle-ci si nécessaire."""
        self._objects.append(objectToAdd)
        self._dimension.resizeToInclude(
            objectToAdd.potentialCollisionZone(self._timeInterval)
        )

        return self

    def _solveFirst(self, timeInterval: float) -> float:
        # recherche du moment de la collision
        checkedInterval = 0
        halfWorkingInterval = timeInterval
        lastCollidedObjects = None
        while halfWorkingInterval > self.timePrecision:

            def getCollidedObjects(objects: List[objects.Object]):
                for first in range(len(objects) - 1):
                    for second in range(first + 1, len(objects)):
                        if objects[first].collides(
                            objects[second], halfWorkingInterval
                        ):
                            return (objects[first], objects[second])
                return None

            collidedObjects = getCollidedObjects(self._objects)

            if collidedObjects:
                lastCollidedObjects = collidedObjects
            else:
                for obj in self._objects:
                    obj.updateReferences(timeInterval)
                if not lastCollidedObjects:
                    # il n'y a aucune collision dans l'intervalle donnée à la fonction
                    return timeInterval
                checkedInterval += halfWorkingInterval
            halfWorkingInterval /= 2

        # gestion de la collision
        # print("Collision entre", lastCollidedObjects[0].formID(), "et", lastCollidedObjects[1].formID())
        point, tangent = lastCollidedObjects[0].collisionPointAndTangent(
            lastCollidedObjects[1]
        )
        angle = tangent.direction()

        masses = [obj.mass() for obj in lastCollidedObjects]
        objSpeeds = [obj.vectorialMotionSpeed() for obj in lastCollidedObjects]
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
            # speedsAfter[current] *= (1 - lastCollidedObjects[current].friction()) * (
            #     1 - lastCollidedObjects[other].friction()
            # )
            lastCollidedObjects[current].set_vectorialMotionSpeed(speedsAfter[current])

            other = current

        return checkedInterval

    def resolve(self) -> None:
        while self._timeInterval > 0:
            self._timeInterval -= self._solveFirst(self._timeInterval)
