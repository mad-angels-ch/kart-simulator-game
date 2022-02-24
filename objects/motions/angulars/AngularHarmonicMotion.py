from logging import warning
import math
from .AngularMotion import AngularMotion
import lib


class AngularHarmonicMotion(AngularMotion):
    """Classe exprimant un movement harmoniques simples.
    Peut être dérivée pour exprimé des mouvements harmoniques plus complexes.\n
    Le centre de rotation est relatif au centre de l'objet associé, et pour des raisons pratiques est exprimé à l'aide d'un vecteur."""

    precision = 1e-6

    _speed: float
    _angularFrequency: float
    _amplitude: float
    _phase: float
    _center: lib.Point
    _static: bool

    def __init__(self, period: float = 0, amplitude: float = 0, phase: float = 0,  center=lib.Point()) -> None:
        self._angularFrequency = 2*math.pi*1/period
        self._amplitude = amplitude
        self._center = center
        self._phase = phase
        self._speed = self.speed()
        
        self.updateIsStatic()

    def updateReferences(self, deltaTime: float) -> None:
        """Avance les références: avance de deltaTime le temps écoulé depuis le lancement de l'oscillation"""
        self._speed = self.speed(deltaTime)
        self._phase = self.phase(deltaTime)
        self.updateIsStatic()
    
    def speed(self, deltaTime: float = 0) -> float:
        """Vitesse vectorielle à l'instant donné"""
        return self.amplitude() * self.angularFrequency() * math.cos(self.phase(deltaTime))

    def angularFrequency(self, deltaTime: float = 0) -> float:
        """Retourne la fréquence angulaire au temps donné"""
        return self._angularFrequency
    
    def set_angularFrequency(self, newFrequency: float) -> None:
        """Change la fréquence angulaire instantanée au temps 0"""
        self._angularFrequency = newFrequency
        self.updateIsStatic()
    
    def amplitude(self, deltaTime: float = 0) -> float:
        """Amplitude à l'instant donné"""
        return self._amplitude
    
    def set_amplitude(self, newAmplitude: float) -> None:
        """Chamge l'amplitude instantanée au temps 0"""
        self._amplitude = newAmplitude
        self.updateIsStatic()

    def phase(self, deltaTime: float = 0) -> float:
        """Déphasage é l'instant donné"""
        return (self._phase + self.angularFrequency()*deltaTime) % (2*math.pi)
    
    def set_phase(self, newPhase: float) -> None:
        """Change de déphasage instantané ai temps 0"""
        self._phase = newPhase % (2*math.pi)
    
    def updateIsStatic(self) -> None:
        """Met la propriété lié à isStatic() à jour, appelée automatiquement."""
        self._static = math.isclose(
            self.speed(), 0, abs_tol=self.precision
        ) and math.isclose(self.angularFrequency(), 0, abs_tol=self.precision) and math.isclose(self.amplitude(), 0, abs_tol=self.precision)

    def isStatic(self) -> bool:
        """Retourne vrai si l'objet est immobile (rotation uniquement)"""
        return self._static
