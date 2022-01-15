import math
import lib


class VectorialMotion:
    """Classe exprimant un movement linéaire à vitesse constante.
    Peut être dérivée pour exprimé des mouvements linéaires plus complexes."""

    _speed: lib.Vector
    _static: bool

    def __init__(self, speed: lib.Vector = lib.Vector()) -> None:
        self._speed = speed
        self.updateIsStatic()

    def updateReferences(self, deltaTime: float) -> None:
        """Avance les références: avance l'instant correspondant au temps 0 de deltaTime"""

    def relativePosition(self, deltaTime: float = 0) -> lib.Vector:
        """Retourne la translation durant le temps donné"""
        return self._speed * deltaTime

    def speed(self, deltaTime: float = 0) -> lib.Vector:
        """Vitesse linéaire à l'instant donné"""
        return self._speed

    def set_speed(self, newSpeed: lib.Vector) -> None:
        """Change la vitesse instantanée au temps 0"""
        self._speed = newSpeed
        self.updateIsStatic()

    def acceleration(self, deltaTime: float = 0) -> lib.Vector:
        """Retourne l'accélération au temps donné"""
        return lib.Vector()

    def set_acceleration(self, newAcceleration: lib.Vector) -> None:
        """Change l'accélération instantanée au temps 0"""
        raise RuntimeError("You can't change the vectorial acceleration of this object")

    def updateIsStatic(self) -> None:
        """Met la propriété lié à isStatic() à jour, appelée automatiquement."""
        self._static = self._speed == lib.Vector()

    def isStatic(self) -> bool:
        """Retourne vrai si l'objet est immobile (rotation uniquement)"""
        return self._static
