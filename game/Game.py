from logging import error, warning
from typing import List
import json
import time

from . import events, objects
from .objects import create as Factory
from .CollisionsZone import CollisionsZone


class Game:
    _events: List[events.Event]
    _output: "function"
    _dataUrl: str
    _objects: List[objects.Object]

    _frameTimer: float
    _gameTimer: float
    _updateGameTimer: bool

    def __init__(
        self, dataUrl: str, events: List[events.Event], output: "function"
    ) -> None:
        self._dataUrl = dataUrl
        self._events = events
        self._output = output
        self._frameTimer = 0
        self._updateGameTimer = False

        with open(dataUrl, "r") as data:
            jsonObject = json.load(data)
            self._objects = Factory.fromFabric(
                jsonObject["objects"], jsonObject["version"]
            )

    def startGameTimer(self, startAt: float = 0) -> None:
        """Démarre le timer du jeu, indépendant de l'instanciation de la partie"""
        self._updateGameTimer = True
        self._gameTimer = startAt

    def resumeGameTimer(self) -> None:
        """Reprend le timer du jeu, indépendant de l'instanciation de la partie"""
        self._updateGameTimer

    def stopGameTimer(self) -> None:
        """Arrête le timer du jeu, indépendant de l'instanciation de la partie"""
        self._updateGameTimer = False

    def nextFrame(self, elapsedTime: float) -> None:
        if elapsedTime > 1 / 50:
            # warning(f"ElapsedTime too big: {elapsedTime}")
            elapsedTime = 1 / 60
        self._frameTimer += elapsedTime
        if self._updateGameTimer:
            self._gameTimer += elapsedTime

        for obj in self._objects:
            obj.onFrameStart(elapsedTime)

        # 1: traiter les events
        self.handleEvents(elapsedTime=elapsedTime)

        # 2: appliquer la physique sur les objects
        self._simulatePhysics(elapsedTime)

        # 3: appeler output
        self.callOutput()

        for obj in self._objects:
            obj.onFrameEnd(elapsedTime)

    def handleEvents(self, elapsedTime: float) -> None:
        for event in self._events:
            if isinstance(event, events.EventOnTarget):
                event.apply(self._objects)
                self._events.remove(event)
            else:
                raise ValueError(f"{event} is not from a supported event type")
        for obj in self._objects:
            obj.onEventsRegistered(deltaTime=elapsedTime)

    def _simulatePhysics(self, elapsedTime: float) -> None:
        zones, others = CollisionsZone.create(self._objects, elapsedTime)
        for zone in zones:
            zone.resolve()
        for other in others:
            other.updateReferences(elapsedTime)

    def callOutput(self) -> None:
        self._output(self._objects)
