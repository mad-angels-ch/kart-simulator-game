from .EventOnTarget import EventOnTarget


class Kart:
    """Sert uniquement à indiquer de type d'éléments cibles attendus et éviter une importation inutile"""


class KartMoveEvent(EventOnTarget):
    """Evènement demandant la mise en mouvement avant-arrière des karts.\n
    L'argument direction fonctionne de la manière suivante:
    -1 = en arrière, 0 = arrêté, 1 = en avant"""

    _direction: int

    def __init__(
        self,
        direction: int,
        targetFormID: "int | None" = None
    ) -> None:
        super().__init__(targetFormID=targetFormID)
        self._direction = direction

    def applyOn(self, target: Kart) -> None:
        target.request_move(self._direction)
