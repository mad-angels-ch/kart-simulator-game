from .EventOnTarget import EventOnTarget


class Kart:
    """Sert uniquement à indiquer de type d'éléments cibles attendus et éviter une importation inutile"""


class KartTurnEvent(EventOnTarget):
    """Evènement demandant la mise en mouvement droite-gauche des karts.\n
    L'argument direction fonction de la manière suivante:
    -1 = à droite, 0 = tout droit, 1 = à gauche"""

    _direction: int

    def __init__(
        self,
        direction: int,
        targetFormID: "int | None" = None
    ) -> None:
        super().__init__(targetFormID=targetFormID)
        self._direction = direction

    def applyOn(self, target: Kart) -> None:
        target.request_turn(self._direction)
