from logging import warning
import math
from game.objects.motions.vectorials.VectorialMotion import VectorialMotion

import lib


class VectorialHarmonicMotion(VectorialMotion):
    """Classe exprimant un movement harmoniques simples.
    Peut être dérivée pour exprimé des mouvements harmoniques plus complexes.\n
    Le centre de rotation est relatif au centre de l'objet associé, et pour des raisons pratiques est exprimé à l'aide d'un vecteur."""

    precision = 1e-6

    _speed: lib.Vector
    _angularFrequency: float
    _amplitude: lib.Vector
    _phase: float
    _static: bool

    def __init__(self, frequency: float = 0, amplitude: lib.Vector = lib.Vector(), phase: float = 0) -> None:
        self._angularFrequency = 2*math.pi*frequency
        self._amplitude = amplitude
        self._phase = phase
        self._speed = self.speed()
        self.updateIsStatic()

    def updateReferences(self, deltaTime: float) -> None:
        """Avance les références: avance de deltaTime le temps écoulé depuis le lancement de l'oscillation"""
        self._speed = self.speed(deltaTime)
        self._phase = self.phase(deltaTime)
        self.updateIsStatic()

    def relativePosition(self, deltaTime: float = 0) -> lib.Vector:
        """Retourne la translation durant le temps donné"""
        return self.amplitude() * math.sin(self.phase(deltaTime))

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
    
    def set_amplitude(self, newAmplitude: lib.Vector) -> None:
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
        self._static = self.speed() == lib.Vector()

    def isStatic(self) -> bool:
        """Retourne vrai si l'objet est immobile (rotation uniquement)"""
        return self._static