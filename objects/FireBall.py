import lib
from .Circle import Circle, Object


class FireBall(Circle):
    """Classe des boules de feu. Le principe est simple: dès qu'un kart touche la boule de feu, il a perdu!"""

    baseSpeed = 500
    spawnDistance = 40
    defaultRadius = 10

    def __init__(self, **kwargs) -> None:
        kwargs["radius"] = kwargs.get("radius", FireBall.defaultRadius)
        kwargs["mass"] = kwargs.get("mass", 1)
        super().__init__(**kwargs)

    def onCollision(self, other: "Object") -> None:
        super().onCollision(other)
        self.destroy()
