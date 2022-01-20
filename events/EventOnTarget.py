from typing import Any, List

from .Event import Event, Object


class EventOnTarget(Event):
    """Evènement destinné à un ou plusieurs objets.
    Sert notamment à transmettre les inputs des utilisateurs aux objets associés.\n
    Ne pas utiliser directement, mais dériver et surchager le constructeur ainsi que la méthode applyOn()."""

    _target: Any
    _method: str

    def __init__(
        self, targetFormID: "int | None" = None, targetsName: "str | None" = None
    ) -> None:
        super().__init__()
        if targetFormID:
            self._method = "formID"
            self._target = targetFormID
        elif targetsName:
            self._method = "name"
            self._target = targetsName
        else:
            raise KeyError("Neither targetFormID or targetsName was given")

    def method(self) -> str:
        """Retourne la méthode d'itentification de la ou les cibles"""
        return self._method

    def target(self) -> Any:
        """Retourne la clé permettant l'identification, dépendant de la méthode"""
        return self._target

    def apply(self, objects: List[Object]):
        """NE PAS SURCHARGER, sert à sélectionner les éléments cibles et appele applyOn() sur ceux-ci"""
        for obj in objects:
            if self.method() == "formID" and obj.formID() == self.target():
                self.applyOn(obj)
            elif self.method() == "name" and obj.name() == self.target():
                self.applyOn(obj)

    def applyOn(self, target: Object) -> None:
        """Méthode à surcharger.
        Lors du traitement des évènements, cette méthode est appliqué sur chaques objets cibles, passés comme argument"""