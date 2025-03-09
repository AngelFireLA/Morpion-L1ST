
class Partie:

    def __init__(self):
        self.grille = [[None for _ in range(3)] for _ in range(3)]
        self.joueur1 = None
        self.joueur2 = None
        self.tour_joueur = 1

    def ajouter_joueur(self, joueur):
        if not self.joueur1:
            self.joueur1 = joueur
        elif not self.joueur2:
            self.joueur2 = joueur
        else:
            raise ValueError("La partie est déjà pleine")

    def jouer(self, coup, num_joueur):
        if num_joueur != self.tour_joueur:
            print("Ce n'est pas votre tour")
            return
        if num_joueur == 1:
            symbole = self.joueur1.symbole
        elif num_joueur == 2:
            symbole = self.joueur2.symbole
        else:
            raise ValueError("Joueur inconnu")
        if not (coup[0] in range(3) and coup[1] in range(3)):
            raise IndexError("Coup invalide", coup)
        if self.grille[coup[1]][coup[0]] is not None:
            raise IndexError("Cette case est déjà occupée")
        self.grille[coup[1]][coup[0]] = symbole

