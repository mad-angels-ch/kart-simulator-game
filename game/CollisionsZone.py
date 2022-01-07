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
        zones: List[CollisionsZone] = []
        objs = [o for o in objectsList if o.isStatic()] + [
            o for o in objectsList if not o.isStatic()
        ]
        current = -1
        # ne pas tester le dernier objet contre lui-même
        while -current < len(objs) and not objs[current].isStatic():
            tested = 0
            while tested < len(objs) + current:
                if (
                    objs[current]
                    .potentialCollisionZone(timeInterval)
                    .collides(objs[tested].potentialCollisionZone(timeInterval))
                ):
                    obj = objs.pop(tested)
                    zones.append(CollisionsZone(timeInterval, objs.pop(current), obj))
                    # nous avons supprimé l'objet mettre <current> à jour (car c'est l'index par rapport à la fin de la liste)
                    current += 1
                    if not obj.isStatic():
                        # les objets statics déjà testés peuvent entrer en collision avec le nouvel objet en mvt
                        tested = 0
                    # pas besoin d'incrémenter <tested> car l'objet a été supprimé
                    # ajouter maintenant le reste des objets à la zone en suivant la même logique
                    while tested < len(objs):
                        if zones[-1].collides(objs[tested]):
                            obj = objs.pop(tested)
                            zones[-1] += obj
                            if not obj.isStatic():
                                tested = 0
                        tested += 1
                    break
                tested += 1
            current -= 1

        return zones, objs

    _timeInterval: float
    _objects: List[objects.Object]
    _dimension: lib.AlignedRectangle
    _movingDimension: lib.AlignedRectangle

    def __init__(self, timeInterval: float, *objectsInside: objects.Object) -> None:
        super().__init__()
        self._timeInterval = timeInterval
        if len(objectsInside) < 2:
            raise SyntaxError("A collision zone must contain at least 2 objects")
        elif objectsInside[0].isStatic():
            raise ValueError("The first object can't be static")
        self._objects = [objectsInside[0]]
        self._dimension = objectsInside[0].potentialCollisionZone(timeInterval).copy()
        self._movingDimension = self._dimension.copy()
        for obj in objectsInside[1:]:
            self += obj

    def __iadd__(self, objectToAdd: objects.Object) -> "CollisionsZone":
        """Ajoute un objet à la zone et redimentionne celle-ci si nécessaire"""
        self._objects.append(objectToAdd)
        self._dimension.resizeToInclude(
            objectToAdd.potentialCollisionZone(self._timeInterval)
        )
        if not objectToAdd.isStatic():
            self._movingDimension.resizeToInclude(
                objectToAdd.potentialCollisionZone(self._timeInterval)
            )
        return self

    def collides(self, objectToCheck: objects.Object) -> bool:
        """Retourne vrai si l'objet donné en paramètre se trouve dans la zone."""
        if objectToCheck.isStatic():
            return self._movingDimension.collides(
                objectToCheck.potentialCollisionZone(self._timeInterval)
            )
        else:
            return self._dimension.collides(
                objectToCheck.potentialCollisionZone(self._timeInterval)
            )

    def __iadd__(self, objectToAdd: objects.Object) -> None:
        """Ajoute un objet à la zone et redimensionne celle-ci si nécessaire."""
        self._objects.append(objectToAdd)
        # objectCollisionZone: lib.AlignedRectangle = objectToAdd.potentialCollisionZone()

        return self

    def _solveFirst(self, timeInterval: float) -> float:
        # recherche du moment de la collision
        def getCollidedObjects(objects: List[objects.Object]):
            print(halfWorkingInterval)
            for first in range(len(objects) - 1):
                for second in range(first + 1, len(objects)):
                    if objects[first].collides(objects[second], halfWorkingInterval):
                        return (objects[first], objects[second])
            return None

        checkedInterval = 0
        halfWorkingInterval = timeInterval
        lastCollidedObjects = None
        while halfWorkingInterval > self.timePrecision:
            collidedObjects = getCollidedObjects(self._objects)

            if collidedObjects:
                print(collidedObjects[0].collides(collidedObjects[1], 0))
                lastCollidedObjects = collidedObjects
            else:
                for obj in self._objects:
                    obj.updateReferences(halfWorkingInterval)
                if not lastCollidedObjects:
                    # il n'y a aucune collision dans l'intervalle donnée à la fonction
                    return halfWorkingInterval
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
            lastCollidedObjects[current].onCollision(lastCollidedObjects[other])
            lastCollidedObjects[current].set_vectorialMotionSpeed(speedsAfter[current])

            other = current

        print("collision", speedsAfter[0].x())
        return checkedInterval

    def resolve(self) -> None:
        """Détecte précisément les collisions, gère celle-ci et met les objets à jours"""
        while self._timeInterval > 0:
            self._timeInterval -= self._solveFirst(self._timeInterval)
