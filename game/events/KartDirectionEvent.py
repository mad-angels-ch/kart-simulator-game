from .EventOnTarget import EventOnTarget, Object


class Kart:
    pass


class KartDirectionEvent(EventOnTarget):
    # <0 -> droite, 0 -> tout droit, >0 -> gauche
    _direction: int

    def __init__(
        self,
        direction: "int",
        targetFormID: "int | None" = None,
        targetsName: "str | None" = None,
    ) -> None:
        super().__init__(targetFormID=targetFormID, targetsName=targetsName)
        self._direction = direction

    def applyOn(self, target: Kart) -> None:
        pass
