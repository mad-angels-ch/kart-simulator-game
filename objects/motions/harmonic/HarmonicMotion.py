from logging import warning
import math

import lib


class HarmonicMotion:
    """Classe exprimant un movement harmoniques simples.
    Peut être dérivée pour exprimé des mouvements harmoniques plus complexes.\n
    Le centre de rotation est relatif au centre de l'objet associé, et pour des raisons pratiques est exprimé à l'aide d'un vecteur."""

    precision = 1e-6

    _speed: float
    _angularFrequency: float
    _amplitude: float
    _phase: float
    _center: lib.Vector
    _static: bool
    _time: float

    def __init__(self, angularFrequency: float = 0, amplitude: float = 0, phase: float = 0,  center=lib.Vector((0, 0))) -> None:
        self._angularFrequency = angularFrequency
        self._amplitude = amplitude
        self._center = center
        if self._angularFrequency != 0:
            self._time = 0 + phase/self._angularFrequency
        else:
            self._time = 0
        
        self.updateIsStatic()

    def updateReferences(self, deltaTime: float) -> None:
        """Avance les références: avance de deltaTime le temps écoulé depuis le lancement de l'oscillation"""
        self._speed = self.speed(deltaTime)
        self.updateIsStatic()

    def center(self) -> lib.Vector:
        """Centre de rotation. Relatif au centre de l'objet."""
        return self._center

    def set_center(self, newCenter: lib.Vector) -> None:
        """Change le centre de rotation."""
        self._center = newCenter

    def speed(self, deltaTime: float = 0) -> float:
        """Vitesse angulaire à l'instant donné"""
        return self._amplitude * self._angularFrequency * math.cos(self._angularFrequency * (self._time + deltaTime))

    def angularFrequency(self, deltaTime: float = 0) -> float:
        """Retourne l'accélération au temps donné"""
        return 0
    
    def set_angularFrequency(self, newFrequency: float) -> None:
        """Change la vitesse instantanée au temps 0"""
        self._angularFrequency = newFrequency
        self.updateIsStatic()
    
    def amplitude(self, deltaTime: float = 0) -> float:
        """Amplitude à l'instant donné"""
        return self._amplitude
    
    def set_amplitude(self, newAmplitude: float) -> None:
        """Chamge l'amplitude instantanée au temps 0"""
        self._amplitude = newAmplitude
        self.updateIsStatic()

    def updateIsStatic(self) -> None:
        """Met la propriété lié à isStatic() à jour, appelée automatiquement."""
        self._static = math.isclose(
            self.speed(), 0, abs_tol=self.precision
        ) and math.isclose(self.acceleration(), 0, abs_tol=self.precision) and math.isclose(self.amplitude(), 0, abs_tol=self.precision)

    def isStatic(self) -> bool:
        """Retourne vrai si l'objet est immobile (rotation uniquement)"""
        return self._static
