class ObjectFactory:
    """Déclaration pour éviter d'avoir à importer game.objects"""


class Event:
    """Classe abstraite des événements, sert surtout à indiquer le type de variable attendue"""

    def fromTuple(eventTuple: tuple) -> "Event":
        """Retourne l'événement décrit par le tuple"""

    def apply(self, factory: ObjectFactory) -> None:
        """Méthode lancé lors de la réception des évènements, surchargeable."""

    def toTuple(self) -> tuple:
        """Export l'événement en un tuple python"""
