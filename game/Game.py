from typing import List
import json

from .events.Event import Event
from . import objects

from kivy.core.window import Window


class Game:

    from user_actions import keyboard_closed, on_keyboard_down, on_touch_up, on_keyboard_up, on_touch_down




    _events: List[Event]
    _output: "function"
    _dataUrl: str
    _objects: List[objects.Object]
    
    def __init__(self, dataUrl: str, events: List[Event], output: "function") -> None:
        self._dataUrl = dataUrl
        self._events = events
        self._output = output

        with open(dataUrl, "r") as data:
            self._objects = objects.create.fromFabric(json.load(data))


        self._keyboard = Window.request_keyboard(self.keyboard_closed, self)
        self._keyboard.bind(on_key_down=self.on_keyboard_down)
        self._keyboard.bind(on_key_up=self.on_keyboard_up)


    def nextFrame(self, elapsedTime: float) -> None:
        # 1: traiter les events
        self.handleEvents()

        # 2: appliquer la physique sur les objects
        self.simulatePhysics(elapsedTime)

        # 3: appeler output
        self.callOutput(elapsedTime)

    def handleEvents(self) -> None:
        pass

    def simulatePhysics(self, elapsedTime: float) -> None:
        for object in self._objects:
            object.updateReferences(elapsedTime)
            
        for i in range(len(self._objects) - 1):
            for ii in range(i + 1, len(self._objects)):
                if self._objects[i].collides(self._objects[ii]):
                    print(f"Collision entre {self._objects[i].formID()} et {self._objects[ii].formID()}")

    def callOutput(self, elapsedTime: float) -> None:
        self._output(elapsedTime, self._objects)
