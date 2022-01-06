from .EventOnTarget import EventOnTarget


class Kart:
    pass


class KartMoveEvent(EventOnTarget):
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
