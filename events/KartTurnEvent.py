from .Event import Event, ObjectFactory


class KartTurnEvent(Event):
    """Evènement demandant la mise en mouvement droite-gauche des karts.\n
    L'argument direction fonction de la manière suivante:
    -1 = à droite, 0 = tout droit, 1 = à gauche"""

    _direction: int
    _kart: int

    def fromTuple(eventTuple: tuple) -> "Event":
        return KartTurnEvent(*tuple)

    def __init__(self, direction: int, kart: int) -> None:
        super().__init__()
        self._direction = direction
        self._kart = kart

    def apply(self, factory: ObjectFactory) -> None:
        factory[self._kart].request_turn(self._direction)

    def toTuple(self) -> tuple:
        return (self._direction, self._kart)
