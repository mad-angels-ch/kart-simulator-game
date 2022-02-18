from typing import Any, List
from game.objects import Flipper

from game.objects.ObjectFactory import ObjectFactory

from .Event import Event, Object


class EventOnTarget(Event):
    """Evènement destinné à un ou plusieurs objets.
    Sert notamment à transmettre les inputs des utilisateurs aux objets associés.\n
    Ne pas utiliser directement, mais dériver et surchager le constructeur ainsi que la méthode applyOn()."""

    _target: Any

    def __init__(
        self, targetFormID: int = None,
        targetsName = None
    ) -> None:
        super().__init__()
        if targetFormID:
            self._targetID = targetFormID
            self._targetsName = None
        elif targetsName:
            self._targetsName = targetsName
            self._targetID = None
        else:
            raise KeyError("No targetFormID was given")

    def targetID(self) -> Any:
        """Retourne la clé permettant l'identification"""
        return self._targetID
    
    def targetsName(self):
        return self._targetsName

    def apply(self, factory: ObjectFactory):
        """NE PAS SURCHARGER, sert à sélectionner les éléments cibles et appele applyOn() sur ceux-ci"""
        if self._targetsName in ["rightFlipper", "leftFlipper"]:
            for flipper in factory.objectsByType(Flipper):
                if flipper.name() == self.targetsName():
                    self.applyOn(flipper)
        else:
            for obj in factory.objects():
                if obj.formID() == self.targetID():
                    self.applyOn(obj)

    def applyOn(self, target: Object) -> None:
        """Méthode à surcharger.
        Lors du traitement des évènements, cette méthode est appliqué sur chaques objets cibles, passés comme argument"""
