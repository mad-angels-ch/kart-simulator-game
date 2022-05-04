from .Event import Event
from .FlipperEvent import FlipperEvent
from .KartMoveEvent import KartMoveEvent
from .KartTurnEvent import KartTurnEvent
from .FireBallEvent import FireBallEvent

eventsByName = {
    ev.__name__: ev
    for ev in (Event, FlipperEvent, KartMoveEvent, KartTurnEvent, FireBallEvent)
}
