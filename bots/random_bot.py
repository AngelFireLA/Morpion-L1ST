from .bot import Bot
from ..utils import coups_légaux
import random


class RandomBot(Bot):
    def __init__(self, nom, symbole):
        super().__init__(nom, symbole)

    def trouver_coup(self, grille):
        return random.choice(coups_légaux(grille))