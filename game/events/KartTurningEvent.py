from .EventOnTarget import EventOnTarget, Object


class Kart:
    pass


class KartTurningEvent(EventOnTarget):
    # <0 -> droite, 0 -> tout droit, >0 -> gauche
    _turning: int

    def __init__(
        self,
        turning: "int",
        targetFormID: "int | None" = None,
        targetsName: "str | None" = None,
    ) -> None:
        super().__init__(targetFormID=targetFormID, targetsName=targetsName)
        self._turning = turning

    def applyOn(self, target: Kart) -> None:
        target.addTurning(self._turning)
