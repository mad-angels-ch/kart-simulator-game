from logging import warning
import math

import lib


class AngularMotion:
    """Classe exprimant un movement angulaire à vitesse constante.
    Peut être dérivée pour exprimé des mouvements angulaires plus complexes.\n
    Le centre de rotation est relatif au centre de l'objet associé, et pour des raisons pratiques est exprimé à l'aide d'un vecteur."""

    precision = 1e-6

    _speed: float
    _center: lib.Vector
    _static: bool

    def __init__(self, speed: float = 0, center=lib.Vector((0, 0))) -> None:
        self._speed = speed
        self._center = center
        self.updateIsStatic()

    def updateReferences(self, deltaTime: float) -> None:
        """Avance les références: avance l'instant correspondant au temps 0 de deltaTime"""

    def center(self) -> lib.Vector:
        """Centre de rotation. Relatif au centre de l'objet."""
        return self._center

    def set_center(self, newCenter: lib.Vector) -> None:
        """Change le centre de rotation."""
        self._center = newCenter

    def relativeAngle(self, deltaTime: float = 0) -> float:
        """Retourne la rotation (sens anti-horaire) durant le temps donné"""
        return self._speed * deltaTime

    def speed(self, deltaTime: float = 0) -> float:
        """Vitesse angulaire à l'instant donné"""
        return self._speed

    def set_speed(self, newSpeed: float) -> None:
        """Change la vitesse instantanée au temps 0"""
        self._speed = newSpeed
        self.updateIsStatic()

    def acceleration(self, deltaTime: float = 0) -> float:
        """Retourne l'accélération au temps donné"""
        return 0

    def set_acceleration(self, newAcceleration: float) -> None:
        """Change l'accélération instantanée au temps 0"""
        raise RuntimeError("You can't change the angular acceleration of this object")

    def updateIsStatic(self) -> None:
        """Met la propriété lié à isStatic() à jour, appelée automatiquement."""
        self._static = math.isclose(
            self.speed(), 0, abs_tol=self.precision
        ) and math.isclose(self.acceleration(), 0, abs_tol=self.precision)

    def isStatic(self) -> bool:
        """Retourne vrai si l'objet est immobile (rotation uniquement)"""
        return self._static
