from typing import Any, List

from .Event import Event, Object


class EventOnTarget(Event):
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
        """Retourne la méthode d'itentification de la cible"""
        return self._target

    def target(self) -> Any:
        """Retourne la clé permettant l'identification, dépendant de la méthode"""
        return self._target

    def apply(self, objects: List[Object]):
        """Méthode à ne pas surcharger, sert à sélectionner les éléments cibles"""
        for obj in objects:
            if obj[self.method()]() == self.target():
                self.applyOn(obj)

    def applyOn(self, target: Object) -> None:
        """Méthode à surcharger"""
        pass
