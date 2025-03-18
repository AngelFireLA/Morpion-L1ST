from ..utils import coups_légaux
import random


class Bot:
    def __init__(self, nom, symbole):
        self.nom = nom
        self.symbole = symbole

    def trouver_coup(self, grille):
        return coups_légaux(grille)[0]
