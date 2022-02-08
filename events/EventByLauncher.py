from typing import Any, List

from game.objects.motions.vectorials.VectorialMotion import VectorialMotion

from .Event import Event
from game.objects import Object


class EventByLauncher(Event):
    """Evènement destinné à un ou plusieurs objets.
    Sert notamment à transmettre les inputs des utilisateurs aux objets associés.\n
    Ne pas utiliser directement, mais dériver et surchager le constructeur ainsi que la méthode applyOn()."""

    _launcher: Any
    _method: str

    def __init__(
        self, launcherFormID: "int | None" = None, launchersName: "str | None" = None
    ) -> None:
        super().__init__()
        if launcherFormID:
            self._method = "formID"
            self._launcher = launcherFormID
        elif launchersName:
            self._method = "name"
            self._launcher = launchersName
        else:
            raise KeyError("Neither launcherFormID or launchersName was given")

    def method(self) -> str:
        """Retourne la méthode d'itentification de la ou les cibles"""
        return self._method

    def launcher(self) -> Any:
        """Retourne la clé permettant l'identification, dépendant de la méthode"""
        return self._launcher

    def apply(self, objects: List[Object]):
        """NE PAS SURCHARGER, sert à sélectionner les éléments cibles et appele createFrom() sur ceux-ci"""
        for obj in objects:
            if self.method() == "formID" and obj.formID() == self.launcher():
                velocity = obj.vectorialMotionSpeed()*1.5
                if velocity.norm() != 0 and obj.FireBallsLaunched < obj.maxFireBalls:
                    objects.append(self.createFrom(launcherObject=obj, velocity=velocity))
            elif self.method() == "name" and obj.name() == self.launcher():
                velocity = obj.vectorialMotionSpeed()*1.5
                if velocity.norm() != 0 and obj.FireBallsLaunched < obj.maxFireBalls:
                    objects.append(self.createFrom(launcherObject=obj, velocity=velocity))

    def createFrom(self, launcherObject: Object, velocity: VectorialMotion) -> None:
        """Méthode à surcharger.
        Lors du traitement des évènements, cette méthode est appliqué sur chaques objets cibles, passés comme argument"""
