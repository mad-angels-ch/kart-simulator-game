class ObjectFactory:
    """Déclaration pour éviter d'avoir à importer game.objects"""


class Event:
    """Classe abstraite des événements, sert surtout à indiquer le type de variable attendue"""

    def apply(self, factory: ObjectFactory) -> None:
        """Méthode lancé lors de la réception des évènements, surchargeable."""
