from .Event import Event, ObjectFactory


class FlipperEvent(Event):
    """Evènement demandant la mise en mouvement des flippers."""

    _upward: bool
    _name: str

    def __init__(self, upward: bool, name: str) -> None:
        super().__init__()
        self._upward = upward
        self._name = name

    def apply(self, factory: ObjectFactory) -> None:
        factory.objectsByName(self._name).addMovement(self._upward)
