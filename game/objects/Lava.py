import lib

from .Polygon import Object, Polygon


class Lava(Polygon):
    """Classe de la lave. Le principe est simple: dès qu'un kart touche la lave, il a perdu!"""
