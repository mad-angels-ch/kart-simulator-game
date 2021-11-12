from .EventOnTarget import EventOnTarget, Object


class Kart:
    pass


class KartAccelerationEvent(EventOnTarget):
    # <0 -> ralentir (freins / reculer), 0 -> frottements seulement, >0 -> accélérer
    _acceleration: int

    def __init__(
        self,
        acceleration: "int",
        targetFormID: "int | None" = None,
        targetsName: "str | None" = None,
    ) -> None:
        super().__init__(targetFormID=targetFormID, targetsName=targetsName)
        self._acceleration = acceleration

    def applyOn(self, target: Kart) -> None:
        pass
