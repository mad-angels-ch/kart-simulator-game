from .EventOnTarget import EventOnTarget


class Kart:
    pass


class KartTurnEvent(EventOnTarget):
    """Event permettant de faire tourner le kart correspondant.\n
    <direction>: -1 = à droite, 0 = tout droit, 1 = à gauche"""

    _direction: int

    def __init__(
        self,
        direction: int,
        targetFormID: "int | None" = None,
        targetsName: "str | None" = None,
    ) -> None:
        super().__init__(targetFormID=targetFormID, targetsName=targetsName)
        self._direction = direction

    def applyOn(self, target: Kart) -> None:
        target.request_turn(self._direction)
