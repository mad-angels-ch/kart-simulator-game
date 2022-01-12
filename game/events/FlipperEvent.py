from .EventOnTarget import EventOnTarget, Object


class Flipper:
    """Sert uniquement à indiquer de type d'éléments cibles attendus et éviter une importation inutile"""


class FlipperEvent(EventOnTarget):
    """Evènement demandant la mise en mouvement des flippers."""

    _upward: bool

    def __init__(
        self,
        upward: bool,
        targetFormID: "int | None" = None,
        targetsName: "str | None" = None,
    ) -> None:
        super().__init__(targetFormID=targetFormID, targetsName=targetsName)
        self._upward = upward

    def applyOn(self, target: Flipper) -> None:
        target.addMovement(self._upward)
