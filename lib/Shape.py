class Shape:
    """Classe parent pour tous les formes géométriques, sert à donner les méthodes communes."""

    def copy(self) -> "Shape":
        """Retourne une copie"""
        raise RuntimeError()

    def collides(self, other: "Shape") -> bool:
        """Retourne vrai s'ils se coupent ou touchent"""
        raise RuntimeError()