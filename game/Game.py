from logging import error
from typing import List
import json
import time

from . import events, objects
from .CollisionsZone import CollisionsZone

from kivy.core.window import Window


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
            self._objects = objects.create.fromFabric(json.load(data))


    # def to_window(self, x, y, initial=False, relative=False):
    #     return super().to_window(x, y, initial=initial, relative=relative)
    # i = 0
    def nextFrame(self, elapsedTime: float) -> None:
        # self.i += 1
        # print("update"+str(self.i)+", please wait.........\n")

        if elapsedTime > 1 / 50:
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
        collisionsZone = CollisionsZone(elapsedTime)
        for object in self._objects:
            collisionsZone += object
        collisionsZone.resolve()

    def callOutput(self) -> None:
        self._output(self._objects)
