from .Event import Event, ObjectFactory


class KartMoveEvent(Event):
    """Evènement demandant la mise en mouvement avant-arrière des karts.\n
    L'argument direction fonctionne de la manière suivante:
    -1 = en arrière, 0 = arrêté, 1 = en avant"""

    _direction: int
    _kart: int

    def __init__(self, direction: int, kart: int) -> None:
        super().__init__()
        self._direction = direction
        self._kart = kart

    def apply(self, factory: ObjectFactory) -> None:
        factory[self._kart].request_move(self._direction)
