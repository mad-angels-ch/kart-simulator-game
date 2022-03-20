from logging import error, warning
from typing import Callable, List, Tuple
import json
import time

import lib

from . import events
from .objects import Object, ObjectFactory
from .objects.ObjectFactory import ObjectFactory
from .CollisionsZone import CollisionsZone, OnCollisionT


class Game:
    _output: Callable[[List[Object]], None]
    _onCollision: OnCollisionT
    _factory: ObjectFactory

    def __init__(
        self,
        fabric: str,
        output: Callable[[List[Object]], None],
        onCollision: OnCollisionT = lambda o, p: None,
    ) -> None:
        self._output = output
        self._onCollision = onCollision
        self._factory = ObjectFactory(fabric)

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
            event.apply(self._factory)
        for obj in self._factory.objects():
            obj.onEventsRegistered(deltaTime=elapsedTime)

    def _simulatePhysics(self, elapsedTime: float) -> None:
        """Attention, c'est là que ça se passe!"""
        zones, others = CollisionsZone.create(self._factory.objects(), elapsedTime)
        for zone in zones:
            zone.resolve()
        for other in others:
            other.updateReferences(elapsedTime)

    def callOutput(self) -> None:
        """Met l'affichage à jour"""
        self._output(self._factory.objects())
