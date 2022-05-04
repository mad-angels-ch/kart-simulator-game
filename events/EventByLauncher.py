from plistlib import FMT_XML
from typing import Any, List
from game.objects.ObjectFactory import ObjectFactory

from game.objects.motions.vectorials.VectorialMotion import VectorialMotion

from .Event import Event
from game.objects import Object


class EventByLauncher(Event):
    """Evènement destinné à un ou plusieurs objets.
    Sert notamment à transmettre les inputs des utilisateurs aux objets associés.\n
    Ne pas utiliser directement, mais dériver et surchager le constructeur ainsi que la méthode apply()."""

    _launcher: Any

    def __init__(
        self, launcherFormID: "int | None"
        ) -> None:
        super().__init__()
        self._launcher = launcherFormID

    def launcher(self) -> Any:
        """Retourne la clé permettant l'identification"""
        return self._launcher

    def apply(self, Factory: ObjectFactory):
        """NE PAS SURCHARGER, sert à sélectionner les éléments cibles et appele create() de ObjectFactory sur ceux-ci"""
        obj=Factory.objectsDict().get(self.launcher())
        velocity = obj.vectorialMotionSpeed()*1.5
        if velocity.norm() != 0 and obj.fireBallsLaunched() < obj.maxFireBalls():
            Factory.create("FireBall", **self.createCharacteristics(launcherObject=obj, velocity=velocity))

    def createCharacteristics(self, launcherObject: Object, velocity: VectorialMotion) -> None:
        """Méthode à surcharger.
        Lors du traitement des évènements, cette méthode est appliqué sur l'objet cible, passé comme argument"""
