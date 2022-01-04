import math
from typing import List
import lib

from .Polygon import Polygon
from .motions import angulars as angularMotions, vectorials as vectorialMotions


class Kart(Polygon):
    forwardAcceleration = 10
    backwardAcceleration = 10
    _turning = 1

    _accelerationsQueue: List[int]
    _turningQueue: List[int]
    _isTurning: int

    def __init__(self, **kwargs) -> None:
        super().__init__(**kwargs)
        self._vectorialMotion = vectorialMotions.UniformlyAcceleratedMotion()
        self._accelerationsQueue = []
        self._turningQueue = []
        self._isTurning = 0

    def addAcceleration(self, acceleration: int) -> None:
        """Demande à change "l'accélération" du kart.
        <acceleration> fonctionnne de la manière suivante:
        <0 -> ralentir (freins / reculer), 0 -> frottements seulement, >0 -> accélérer"""
        self._accelerationsQueue.append(acceleration)

    def addTurning(self, turning: int) -> None:
        """Demande à change la "direction" du kart".
        <turning> fonctionnne de la manière suivante:
        <0 -> droite, 0 -> tout droit, >0 -> gauche"""
        self._turningQueue.append(turning)

    def isTurning(self) -> int:
        """Retourne -1 si le kart est en train de tourner à droite,
        0 s'il va tout droit et 1 s'il tourne à gauche"""
        return self._isTurning

    def updateReferences(self, deltaTime: float) -> None:
        super().updateReferences(deltaTime)
        while len(self._accelerationsQueue):
            acceleration = self._accelerationsQueue.pop(0)
            if acceleration > 0:
                acceleration = lib.Vector((0, self.forwardAcceleration))
                acceleration.rotate(self.angle())
                self.set_vectorialMotionAcceleration(acceleration)
                # vx = -math.sin(self.angle()) * self._acceleration.x()
                # vy = math.cos(self.angle()) * self._acceleration.y()
                # v = lib.Vector((vx, vy))
                # self.set_vectorialMotionAcceleration(v)
            elif acceleration < 0:
                acceleration = lib.Vector((0, -self.backwardAcceleration))
                acceleration.rotate(self.angle())
                self.set_vectorialMotionAcceleration(acceleration)
                # vx = math.sin(self.angle()) * self._acceleration.x()
                # vy = -math.cos(self.angle()) * self._acceleration.y()
                # v = lib.Vector((vx, vy))
                # self.set_vectorialMotionAcceleration(v)
            else:
                self.set_vectorialMotionAcceleration(lib.Vector())
        while len(self._turningQueue):
            self._isTurning = self._turningQueue.pop(0)
            if self._isTurning < 0:
                self.vectorialMotionSpeed().rotate(-self._turning * deltaTime)
                speed = lib.Vector(self.vectorialMotionSpeed())
                speed.rotate(-self._turning * deltaTime)
                self.set_vectorialMotionSpeed(speed)
                self.rotate(-self._turning * deltaTime)
            elif self._isTurning > 0:
                self.vectorialMotionSpeed().rotate(-self._turning * deltaTime)
                speed = lib.Vector(self.vectorialMotionSpeed())
                speed.rotate(self._turning * deltaTime)
                self.set_vectorialMotionSpeed(speed)
                self.rotate(self._turning * deltaTime)
                # self.vectorialMotionSpeed().rotate(self._turning * deltaTime)
                # self.rotate(self._turning * deltaTime)
