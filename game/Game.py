from typing import List

from .events.Event import Event


class Game:
    _events: List[Event]
    _output: function

    _dataUrl: str
    _objects: list

    def __init__(self, dataUrl: str, events: List[Event], output: function) -> None:
        self._dataUrl = dataUrl
        self._events = events
        self._output = output

    def nextFrame(self, elapsedTime: float) -> None:
        # 1: traiter les events
        self.handleEvents()

        # 2: appliquer la physique sur les objects
        self.simulatePhysics(elapsedTime)

        # 3: appeler output
        self.callOutput()

    def handleEvents(self) -> None:
        pass

    def simulatePhysics(self, elapsedTime: float) -> None:
        pass

    def callOutput(self) -> None:
        self._output(self._objects)
