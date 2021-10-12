from typing import Any
from lib import Vector

from .Event import Event

class NewAccelerationEvent(Event):
    _author: Any
    _acceleration: Vector

    def __init__(self, newAcceleration: Vector, author: Any) -> None:
        super(NewAccelerationEvent, self).__init__()
        self._author = author
        self._acceleration = newAcceleration