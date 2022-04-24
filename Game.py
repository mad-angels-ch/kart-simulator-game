from logging import error, warning
from typing import Callable, List

from . import events
from .objects import (
    Object,
    ObjectFactory,
    Kart,
    FinishLine,
    onBurnedT,
    onCompletedAllLapsT,
    onPassageT,
)
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
        kart_onBurned: onBurnedT = lambda k: None,
        kart_onCompletedAllLaps: onCompletedAllLapsT = lambda k: None,
        gate_onPassage: onPassageT = lambda g, k: None,
    ) -> None:
        self._output = output
        self._onCollision = onCollision
        self._factory = ObjectFactory(
            fabric, kart_onBurned, kart_onCompletedAllLaps, gate_onPassage
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

        self._factory.clean(elapsedTime)

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
            zone.resolve(self._onCollision)
        for other in others:
            other.updateReferences(elapsedTime)

    def callOutput(self) -> None:
        """Met l'affichage à jour"""
        objects = self._factory.objects()
        if len(objects):
            self._output(objects)

    def minimalExport(self) -> dict:
        """Exporte uniquement les données nécessaires à l'affichage du monde"""
        return self._factory.minimalExport()

    def minimalImport(self, minimalExport: dict) -> None:
        """Charge le minimum de données nécessaires à l'affichage du monde.
        Attent un objet du même format qu'exporté par minimalExport()"""
        self._factory.destroyAll()
        self.callOutput()
        self._factory.clean(0)
        self._factory.minimalImport(minimalExport)
        self.callOutput()

    def objectByFormID(self, formID: int) -> Object:
        return self._factory[formID]

    def karts(self) -> List[Kart]:
        """Retourne la liste des karts (placeholders et instanciés)"""
        return self._factory.karts()

    def kartPlaceholders(self) -> List[Kart]:
        """Retourne la liste des karts placeholder"""
        return self._factory.kartPlaceholders()

    def kartsInGame(self) -> List[Kart]:
        """Retourne la liste des karts actuellement en jeu"""
        return self._factory.kartsInGame()

    def loadKart(self, username: str, img: str, placeHolder: int = None) -> int:
        """Créé un kart à l'emplacement donné par le placeHolder.
        Si le placeHolder n'est pas donné, il est séléctionné au hasard parmis les restants"""
        return self._factory.loadKart(username, img, placeHolder)

    def burnedKarts(self) -> List[Kart]:
        """Retourne tous les karts brûlés"""
        return self._factory.burnedKarts()

    def finishLine(self) -> FinishLine:
        """Nom explicit"""
        return self._factory.finishLine()

    def unloadKart(self, placeHolder: int) -> None:
        """Supprime le kart du jeu, peut à tout moment être recréé avec loadKart()"""
        self._factory.unloadKart(placeHolder)
