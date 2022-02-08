from msilib.schema import LaunchCondition
from game.objects import motions
from game.objects.FireBall import FireBall
from game.objects.motions.vectorials.VectorialMotion import VectorialMotion
from .EventByLauncher import EventByLauncher
from lib import Vector
from .Event import Event, Object
from game.objects.Lava import Lava

class FireBallEvent(EventByLauncher):
    """Evènement demandant la création d'un projectile enflamé.\n
    L'argument vitesse donne la vitesse vectorielle à laquelle est tirée la boule de feu"""

    _vitesse: int

    def __init__(
        self,
        launcherFormID: "int | None" = None,
        launchersName: "str | None" = None,
    ) -> None:
        super().__init__(launcherFormID=launcherFormID, launchersName=launchersName)

    def createFrom(self, launcherObject: Object, velocity: VectorialMotion) -> None:
        position = launcherObject.center().copy()
        position.translate(velocity.unitVector()*40)
        kwds={"vectorialMotion":motions.vectorials.VectorialMotion(velocity), "center":position, "formID":-launcherObject.FireBallsLaunched, "radius":10, "mass": 1}
        launcherObject.FireBallsLaunched += 1
        return FireBall(**kwds)
        