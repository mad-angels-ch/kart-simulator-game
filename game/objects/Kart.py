import math
from typing import List
import lib

from .Polygon import Polygon
from .motions import angulars as angularMotions, vectorials as vectorialMotions


class Kart(Polygon):
    acceleration = 10
    decceleration = -30
    lossesDecceleration = -2
    turning = 1

    _accelerationsQueue: List[int]
    _turningQueue: List[int]

    # 3 -> accelerating forward, 2 -> slowly deccelerating forward, 1 -> brake (while forward)
    # 3 -> accelerating backward, 2 -> slowly deccelerating backward, 1 -> brake (while backward)
    _speedState: int

    def __init__(self, **kwargs) -> None:
        super().__init__(**kwargs)
        self._vectorialMotion = vectorialMotions.UniformlyAcceleratedMotion()
        self._accelerationsQueue = []
        self._turningQueue = []
        self._isTurning = 0
        self._speedState = 0

    def addAcceleration(self, acceleration: int) -> None:
        """Demande à change "l'accélération" du kart.
        <acceleration> fonctionnne de la manière suivante:
        -1 -> ralentir (freins / reculer), 0 -> frottements seulement, 1 -> accélérer"""
        self._accelerationsQueue.append(acceleration)

    def addTurning(self, turning: int) -> None:
        """Demande à change la "direction" du kart".
        <turning> fonctionnne de la manière suivante:
        -1 -> droite, 0 -> tout droit, 1 -> gauche"""
        # self._turningQueue.append(turning)

    def set_vectorialMotionSpeed(self, newSpeed: lib.Vector) -> None:
        super().set_vectorialMotionSpeed(newSpeed)
        self.update()

    def update(self) -> None:
        self._speedState = 2
        while len(self._accelerationsQueue):
            acceleration = self._accelerationsQueue.pop(0)
            if acceleration > 0:
                self._speedState = 3
            elif acceleration < 0:
                self._speedState = 1

        diff = abs(self.angle() - self.vectorialMotionSpeed().direction()) % (
            2 * math.pi
        )
        print(diff)
        if diff <= math.pi / 2 or diff >= 3 * math.pi / 2:
            # print("le kart avance")
            # le kart avance
            pass

        else:
            # print("le kart recule")
            # le kart recule
            self._speedState -= 4

        if self._speedState:
            state = abs(self._speedState)
            if state == 3:
                acceleration = self.acceleration
            elif state == 2:
                acceleration = self.lossesDecceleration
            else:
                acceleration = self.decceleration

            if state < 0:
                acceleration *= -1

            accelerationV = lib.Vector((acceleration, 0))
            accelerationV.rotate(self.angle())
            self.set_vectorialMotionAcceleration(accelerationV)
        else:
            self.set_vectorialMotionAcceleration(lib.Vector())

    def updateReferences(self, deltaTime: float) -> None:
        super().updateReferences(deltaTime)
        self.update()
