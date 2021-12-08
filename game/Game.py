from logging import error, warning
from typing import List
import json
import time

from . import events, objects
from .CollisionsZone import CollisionsZone


class Game:
    _events: List[events.Event]
    _output: "function"
    _dataUrl: str
    _objects: List[objects.Object]

    def __init__(
        self, dataUrl: str, events: List[events.Event], output: "function"
    ) -> None:
        self._dataUrl = dataUrl
        self._events = events
        self._output = output

        with open(dataUrl, "r") as data:
            jsonObject = json.load(data)
            self._objects = objects.create.fromFabric(
                jsonObject["objects"], jsonObject["version"]
            )

    def nextFrame(self, elapsedTime: float) -> None:

        if elapsedTime > 1 / 50:
            warning(f"ElapsedTime too big: {elapsedTime}")
            elapsedTime = 1 / 60

        # 1: traiter les events
        self.handleEvents()

        # 2: appliquer la physique sur les objects
        self.simulatePhysics(elapsedTime)

        # 3: appeler output
        self.callOutput()

    def handleEvents(self) -> None:
        for event in self._events:
            if isinstance(event, events.EventOnTarget):
                event.apply(self._objects)
                self._events.remove(event)
            else:
                raise ValueError(f"{event} is not from a supported event type")

    def simulatePhysics(self, elapsedTime: float) -> None:
        zones, others = CollisionsZone.create(self._objects, elapsedTime)
        for zone in zones:
            zone.resolve()
        for other in others:
            other.updateReferences(elapsedTime)

    def callOutput(self) -> None:
        self._output(self._objects)
