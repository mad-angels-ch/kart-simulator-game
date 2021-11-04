from logging import error
from typing import List
import json
import time

from . import events, objects
from .CollisionsZone import CollisionsZone

from kivy.core.window import Window


class Game:

    from user_actions import (
        keyboard_closed,
        on_keyboard_down,
        on_touch_up,
        on_keyboard_up,
        on_touch_down,
    )

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

        self._keyboard = Window.request_keyboard(self.keyboard_closed, self)
        self._keyboard.bind(on_key_down=self.on_keyboard_down)
        self._keyboard.bind(on_key_up=self.on_keyboard_up)

    def nextFrame(self, elapsedTime: float) -> None:
        if elapsedTime > 1 / 50:
            elapsedTime = 1 / 60

        # 1: traiter les events
        self.handleEvents()

        # 2: appliquer la physique sur les objects
        self.simulatePhysics(elapsedTime)

        # 3: appeler output
        self.callOutput(elapsedTime)

    def handleEvents(self) -> None:
        for event in self._events:
            if isinstance(event, events.EventOnTarget):
                event.apply(self._objects)
            else:
                raise ValueError(f"{event} is not from a supported event type")

    def simulatePhysics(self, elapsedTime: float) -> None:
        collisionsZone = CollisionsZone(elapsedTime)
        for object in self._objects:
            collisionsZone += object
        collisionsZone.resolve()

    def callOutput(self, elapsedTime: float) -> None:
        self._output(elapsedTime, self._objects)
