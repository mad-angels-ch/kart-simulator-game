from logging import error, warning
from typing import List
import json
import time

from . import events, objects
from .objects import create as Factory
from .CollisionsZone import CollisionsZone


class Game:
    _output: "function"
    _dataUrl: str
    _objects: List[objects.Object]

    def __init__(self, dataUrl: str, output: "function") -> None:
        self._dataUrl = dataUrl
        self._output = output
        self._updateGameTimer = False

        with open(dataUrl, "r") as data:
            jsonObject = json.load(data)
            self._objects = Factory.fromFabric(
                jsonObject["objects"], jsonObject["version"]
            )

    def nextFrame(self, elapsedTime: float, newEvents: List[events.Event] = []) -> None:
        """Avance le temps d'<elapsedTime> miliseconde et affiche le jeu à cet instant."""
        if elapsedTime > 1 / 50:
            # warning(f"ElapsedTime too big: {elapsedTime}")
            elapsedTime = 1 / 60

        # 1: traiter les events
        self.handleEvents(elapsedTime=elapsedTime, newEvents=newEvents)

        # 2: appliquer la physique sur les objects
        self._simulatePhysics(elapsedTime)

        # 3: appeler output
        self.callOutput()

    def handleEvents(self, elapsedTime: float, newEvents: List[events.Event]) -> None:
        """Récupère et gère les évènements"""
        for event in newEvents:
            if isinstance(event, events.EventOnTarget):
                event.apply(self._objects)
            else:
                raise ValueError(f"{event} is not from a supported event type")
        for obj in self._objects:
            obj.onEventsRegistered(deltaTime=elapsedTime)

    def _simulatePhysics(self, elapsedTime: float) -> None:
        """Attention, c'est là que ça se passe!"""
        zones, others = CollisionsZone.create(self._objects, elapsedTime)
        for zone in zones:
            zone.resolve()
        for other in others:
            other.updateReferences(elapsedTime)

    def callOutput(self) -> None:
        """Met l'affichage à jour"""
        self._output(self._objects)
