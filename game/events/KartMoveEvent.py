from .EventOnTarget import EventOnTarget


class Kart:
    pass


class KartMoveEvent(EventOnTarget):
    """Event permettant de mettre le kart correspondant en mouvement.\n
    <direction>: -1 = en arrière, 0 = arrêté, 1 = en avant"""

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
        target.request_move(self._direction)
