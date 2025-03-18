import random
import time

from .bot import Bot
from ..utils import coups_légaux, copier_grille, symbole_opposé, vérifier_si_victoire, vérifier_si_match_nul


class Negamax(Bot):
    def __init__(self, nom, symbole):
        super().__init__(nom, symbole)
        self.veut_gagner = True

    def trouver_coup(self, grille, veut_gagner=True):
        self.veut_gagner = veut_gagner
        meilleur_score = -float('inf')
        meilleur_coups = []
        for coup in coups_légaux(grille):
            copie_grille = copier_grille(grille)
            copie_grille[coup[1]][coup[0]] = self.symbole
            score = -self.negamax(copie_grille, -float('inf'), float('inf'), symbole_opposé(self.symbole))
            if score > meilleur_score:
                meilleur_score = score
                meilleur_coups = [coup]
            elif score == meilleur_score:
                meilleur_coups.append(coup)
        print(meilleur_coups, meilleur_score)
        return random.choice(meilleur_coups)

    def grille_à_tuple(self, grille):
        return tuple([tuple(ligne) for ligne in grille])

    def negamax(self, grille, alpha, beta, symbole):
        est_victoire = vérifier_si_victoire(grille)
        est_nul = vérifier_si_match_nul(grille)
        if est_victoire:
            if est_victoire[2] == symbole:
                return 1 if self.veut_gagner else -1
            else:
                return -1 if self.veut_gagner else 1
        if est_nul:
            return 0
        meilleur_score = -float('inf')
        for coup in coups_légaux(grille):
            copie_grille = copier_grille(grille)
            copie_grille[coup[1]][coup[0]] = symbole
            score = -self.negamax(copie_grille, -beta, -alpha, symbole_opposé(symbole))
            meilleur_score = max(meilleur_score, score)
            alpha = max(alpha, score)
            if alpha >= beta:
                break
        return meilleur_score

