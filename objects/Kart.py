from typing import TYPE_CHECKING, Callable

import lib
from .Polygon import Polygon, Object
from .Lava import Lava
from .FireBall import FireBall

if TYPE_CHECKING:
    from .Gate import Gate

onCompletedAllLapsT = Callable[["Kart"], None]
onBurnedT = Callable[["Kart"], None]


class Kart(Polygon):
    """CREER AVEC LA FACTORY\n
    Classe des karts.
    Ceux-ci peuvent être contrôlés à l'aide des méthodes request_move() et request_turn().
    Le sens du kart est indiqué par le vecteur (1, 0) lorsque l'angle du premier vaut 0.
    Les propriétés <movingSpeed> (m/s), <movingCorrectionTime>(s), <turningSpeed>(rad/s) et <turningCorrectionTime> (s)
    peuvent être modifiées et représentent les vitesses maximales et temps de correction du kart."""

    movingSpeed: float = 500
    movingCorrectionTime: float = 0.5
    turningSpeed: float = 4
    turningCorrectionTime: float = 0.2

    # -1 = en arrière, 0 = arrêté, 1 = en avant
    _moving: int

    # -1 = à droite, 0 = tout droit, 1 = à gauche
    _turning: int

    _lastGatePosition: int

    _burned: bool = False
    _completed: bool = False

    _username: str
    _image: str

    _onBurned: onBurnedT
    _onCompletedAllLaps: onCompletedAllLapsT

    def fromMinimalDict(obj: dict) -> dict:
        dic = Polygon.fromMinimalDict(obj)
        dic.update({"onBurned": lambda k: None, "onCompletedAllLaps": lambda k: None})
        return dic

    def __init__(self, **kwargs) -> None:
        kwargs["mass"] = 1
        kwargs["friction"] = 0.6
        super().__init__(**kwargs)
        self._onBurned = kwargs["onBurned"]
        self._onCompletedAllLaps = kwargs["onCompletedAllLaps"]
        self._lastGatePosition = 0
        self._moving = 0
        self._turning = 0
        self._fireBallsLaunched = 0
        self._maxFireBalls = kwargs.get("munitions", 5)
        self._username = kwargs.get("username", "")
        self._image = kwargs.get("image", "")

    def username(self) -> str:
        """Retourne le nom d'utilisateur du joueur du kart"""
        return self._username

    def set_username(self, newUsername: str) -> None:
        """Nom explicite"""
        self._username = newUsername

    def image(self) -> str:
        """Nom de l'image du kart à charger (avec l'extension)"""
        return self._image

    def set_image(self, newImage) -> None:
        """Nom explicite"""
        self._image = newImage

    def fireBallsLaunched(self):
        return self._fireBallsLaunched

    def maxFireBalls(self):
        return self._maxFireBalls

    def add_fireBall(self):
        self._fireBallsLaunched += 1

    def lastGatePosition(self) -> int:
        """Retourne la position du dernier portillon franchis par ce kart"""
        return self._lastGatePosition

    def set_lastGate(self, newLastGame: "Gate") -> None:
        """Modifie le dernier portillon que le kart a traversé"""
        self._lastGatePosition = newLastGame.position()

        # import ici pour éviter des imports circulaires
        from .FinishLine import FinishLine

        if isinstance(newLastGame, FinishLine) and newLastGame.completedAllLaps(
            self.formID()
        ):
            self._completed = True
            self._onCompletedAllLaps(self)

    def hasBurned(self) -> bool:
        """Retourne vrai si le kart s'est fait brûlé par la lave"""
        return self._burned

    def hasCompleted(self) -> bool:
        """Retourne True si le kart a terminé tous ses tours"""
        return self._completed

    def request_move(self, direction: int) -> None:
        """Met le kart en mouvement
        -1 = en arrière, 0 = arrêté, 1 = en avant"""
        self._moving = direction

    def request_turn(self, direction: int) -> None:
        """Fait tourner le kart
        -1 = à droite, 0 = tout droit, 1 = à gauche"""
        self._turning = direction

    def onCollision(self, other: "Object") -> None:
        super().onCollision(other)
        if other.isSolid():
            if isinstance(other, Lava) or isinstance(other, FireBall):
                self._burned = True
                self._onBurned(self)
            self.set_angularMotionSpeed(0)
            self.set_angularMotionAcceleration(0)

    def onEventsRegistered(self, deltaTime: float) -> None:
        if self.hasBurned():
            self._turning = 0
            self._moving = 0
        targetASpeed = self._turning * self.turningSpeed
        currentASpeed = self.angularMotionSpeed()
        self.set_angularMotionAcceleration(
            (targetASpeed - currentASpeed) / self.turningCorrectionTime
        )

        targetVectorialSpeed = lib.Vector((self._moving * self.movingSpeed, 0))
        targetVectorialSpeed.rotate(self.angle())
        currentVectorialSpeed = self.vectorialMotionSpeed()
        acceleration = lib.Vector()
        for i in range(2):
            acceleration[i] = (
                targetVectorialSpeed[i] - currentVectorialSpeed[i]
            ) / self.movingCorrectionTime
        self.set_vectorialMotionAcceleration(acceleration)

    def toMinimalDict(self) -> dict:
        dic = super().toMinimalDict()
        dic.update({"username": self._username, "image": self._image})
        return dic
