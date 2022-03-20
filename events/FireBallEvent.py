from .Event import Event, ObjectFactory


class FireBallEvent(Event):
    """Evènement demandant le lancement d'une boulle de feu"""

    _launcher: int

    def __init__(
        self,
        launcher: int,
    ) -> None:
        super().__init__()
        self._launcher = launcher

    def apply(self, factory: ObjectFactory) -> None:
        factory.createFireBall(self._launcher)
