from .EventOnTarget import EventOnTarget, Object


class Flipper:
    pass


class FlipperEvent(EventOnTarget):
    _upward: bool

    def __init__(
        self,
        upward: bool,
        targetFormID: "int | None" = None,
        targetsName: "str | None" = None,
    ) -> None:
        super().__init__(targetFormID=targetFormID, targetsName=targetsName)
        self._upward = upward

    def upward(self) -> bool:
        """Retourne True si le flipper doit monter ou False s'il doit descendre"""
        return self._up

    def applyOn(self, target: Flipper) -> None:
        target.addMovement(self.upward())
