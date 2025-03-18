import socket
import uuid

import pygame

from ..bots import negamax
from . import menu_pause
from ..moteur.joueur import Joueur
from ..moteur.partie import Partie
from ..utils import largeur_fenetre, hauteur_fenetre, afficher_texte, dict_couleurs, vérifier_si_victoire, \
    vérifier_si_match_nul, coups_légaux, récupérer_ip_cible, récupérer_port, est_local, symbole_opposé, \
    chemin_absolu_dossier

arriere_plan = pygame.image.load(chemin_absolu_dossier+"assets/images/menu_arrière_plan.jpg")
arriere_plan = pygame.transform.scale(arriere_plan, (largeur_fenetre, hauteur_fenetre))


def afficher_plateau(fenetre):
    x_initial = (largeur_fenetre - taille_grille) / 2
    y_initial = (hauteur_fenetre - taille_grille) / 2
    for i in range(1, 3):
        pygame.draw.line(fenetre, dict_couleurs["bleu marin"], (x_initial + i * taille_case, y_initial), (x_initial + i * taille_case, y_initial + taille_grille), 5)
        pygame.draw.line(fenetre, dict_couleurs["bleu marin"], (x_initial, y_initial + i * taille_case), (x_initial + taille_grille, y_initial + i * taille_case), 5)


def afficher_jetons(fenetre, partie):
    grille = partie.grille
    for i in range(len(grille)):
        ligne = grille[i]
        for j in range(len(ligne)):
            jeton = ligne[j]
            if jeton:
                x, y = case_à_position(j, i)
                if jeton == "X":
                    pygame.draw.rect(fenetre, dict_couleurs["noir"], (x + 10, y + 10, taille_case - 20, taille_case - 20), 5)
                else:
                    pygame.draw.circle(fenetre, dict_couleurs["noir"], (x + taille_case // 2, y + taille_case // 2), taille_case // 2 - 10, 5)


def affiche_trucs_de_base(fenetre, partie):
    fenetre.blit(arriere_plan, (0, 0))
    afficher_plateau(fenetre)
    afficher_jetons(fenetre, partie)


def est_tour_bot(partie, veut_gagner) -> bool:
    return partie.tour_joueur == 2 and veut_gagner is not None


def vérifie_fin_de_partie(partie: Partie, fenetre, symbole_joueur, multi=False):
    cases_victoire = vérifier_si_victoire(partie.grille)
    est_nul = vérifier_si_match_nul(partie.grille)
    joueur_actuel = partie.joueur1 if partie.tour_joueur == 1 else partie.joueur2
    if cases_victoire:
        affiche_trucs_de_base(fenetre, partie)
        pygame.display.flip()
        texte_afficher = f"Victoire de {joueur_actuel.nom} !"
        if multi:
            if joueur_actuel.symbole == symbole_joueur:
                texte_afficher = "Victoire !"
            else:
                texte_afficher = "Défaite..."

        x1, y1 = case_à_position(cases_victoire[0][1], cases_victoire[0][0])
        x2, y2 = case_à_position(cases_victoire[1][1], cases_victoire[1][0])

        pygame.draw.line(fenetre, dict_couleurs["noir"], (x1 + taille_case // 2, y1 + taille_case // 2), (x2 + taille_case // 2, y2 + taille_case // 2), 10)
        afficher_texte(fenetre, largeur_fenetre // 2, décalage//2, texte_afficher, 60, dict_couleurs["bleu marin"])
        pygame.display.flip()
        pygame.time.wait(3000)

        return False
    elif est_nul:
        affiche_trucs_de_base(fenetre, partie)
        pygame.display.flip()
        afficher_texte(fenetre, largeur_fenetre // 2, décalage//2, f"Match nul !", 60, dict_couleurs["bleu marin"])
        pygame.display.flip()
        pygame.time.wait(3000)
        return False
    return True


def position_à_case(x, y):
    x_grille_initial = (largeur_fenetre - taille_grille) / 2
    y_grille_initial = (hauteur_fenetre - taille_grille) / 2
    case_x = min((x - x_grille_initial) // taille_case, 2)
    case_y = min((y - y_grille_initial) // taille_case, 2)
    return int(case_x), int(case_y)


def case_à_position(case_x, case_y):
    x_grille_initial = (largeur_fenetre - taille_grille) / 2
    y_grille_initial = (hauteur_fenetre - taille_grille) / 2
    return x_grille_initial + case_x * taille_case, y_grille_initial + case_y * taille_case


décalage = 100
largeur_disponible = largeur_fenetre - 2 * décalage
hauteur_disponible = hauteur_fenetre - 2 * décalage
taille_case = min(largeur_disponible, hauteur_disponible) // 3
taille_grille = taille_case * 3


def main(veut_gagner=None):
    partie = Partie()
    partie.tour_joueur = 1
    clock = pygame.time.Clock()
    joueur1 = Joueur("Joueur 1", "X")
    if veut_gagner is not None:
        joueur2 = negamax.Negamax("Joueur 2", "O")
    else:
        joueur2 = Joueur("Joueur 2", "O")

    partie.ajouter_joueur(joueur1)
    partie.ajouter_joueur(joueur2)
    fenetre = pygame.display.set_mode((largeur_fenetre, hauteur_fenetre))
    pygame.display.set_caption("Partie de Morpion")
    partie_en_cours = True
    while partie_en_cours:
        joueur_actuel = partie.joueur1 if partie.tour_joueur == 1 else partie.joueur2
        for event in pygame.event.get():
            affiche_trucs_de_base(fenetre, partie)
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                case = position_à_case(event.pos[0], event.pos[1])
                if not est_tour_bot(partie, veut_gagner) and case in coups_légaux(partie.grille):
                    partie.jouer(case, partie.tour_joueur)
                    partie_en_cours = vérifie_fin_de_partie(partie, fenetre, joueur_actuel.symbole)
                    if partie.tour_joueur == 1:
                        partie.tour_joueur = 2
                    else:
                        partie.tour_joueur = 1


            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    if menu_pause.main():
                        return
                    else:
                        fenetre = pygame.display.set_mode((largeur_fenetre, hauteur_fenetre))
        affiche_trucs_de_base(fenetre, partie)

        if partie_en_cours:
            if joueur_actuel.symbole == "X":
                pygame.draw.rect(fenetre, (0, 0, 0), (largeur_fenetre - 100, 50, 50, 50), 5)
            else:
                #draw a circle top right corner
                pygame.draw.circle(fenetre, (0, 0, 0), (largeur_fenetre - 100, 50), 20, 5)
            pygame.display.flip()
        clock.tick(60)
        if est_tour_bot(partie, veut_gagner) and partie_en_cours:
            pygame.time.wait(500)
            afficher_texte(fenetre, largeur_fenetre//2, décalage//2, f"{joueur2.nom} réfléchit...", 45, dict_couleurs["bleu marin"])
            pygame.display.flip()
            coup = partie.joueur2.trouver_coup(partie.grille, veut_gagner)
            partie.jouer(coup, partie.tour_joueur)
            partie_en_cours = vérifie_fin_de_partie(partie, fenetre, joueur_actuel.symbole)
            if partie.tour_joueur == 1:
                partie.tour_joueur = 2
            else:
                partie.tour_joueur = 1

def main_multi():
    partie = Partie()
    fenetre = pygame.display.set_mode((largeur_fenetre, hauteur_fenetre))
    pygame.display.set_caption("Partie de Morpion")
    partie.tour_joueur = 1
    clock = pygame.time.Clock()
    port = récupérer_port()
    local = est_local()
    socket_client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    ip_serveur = récupérer_ip_cible() if not local else "127.0.0.1"
    socket_client.connect((ip_serveur, port))
    socket_client.setblocking(False)
    nom_utilisateur = str(uuid.uuid4())
    socket_client.sendall(f"@connexion:{nom_utilisateur}".encode('utf-8'))
    print("Connexion établie")
    fenetre.blit(arriere_plan, (0, 0))
    afficher_texte(fenetre, largeur_fenetre // 2, hauteur_fenetre // 2, "En attente d'un adversaire...", 50, dict_couleurs["bleu marin"])
    pygame.display.flip()
    réponse = ""
    while not réponse.startswith("@commencer:"):
        try:
            réponse = socket_client.recv(2048).decode('utf-8')
        except BlockingIOError:
            pass
        clock.tick(60)
    print("Partie va commencer")
    tour_joueur, nom_adversaire = réponse.split(":")[1].split("|")
    tour_joueur = int(tour_joueur)
    symbole_joueur = "X" if tour_joueur == 1 else "O"
    print(symbole_joueur, tour_joueur, symbole_opposé(symbole_joueur))
    joueur1 = Joueur("Joueur 1", symbole_joueur)
    joueur2 = Joueur("Joueur 2", symbole_opposé(symbole_joueur))

    partie.ajouter_joueur(joueur1)
    partie.ajouter_joueur(joueur2)

    partie_en_cours = True
    while partie_en_cours:
        joueur_actuel = partie.joueur1 if partie.tour_joueur == 1 else partie.joueur2
        for event in pygame.event.get():
            affiche_trucs_de_base(fenetre, partie)
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                case = position_à_case(event.pos[0], event.pos[1])
                if tour_joueur == partie.tour_joueur and case in coups_légaux(partie.grille):
                    partie.jouer(case, partie.tour_joueur)
                    socket_client.sendall(f"@jouer:{case[0]}|{case[1]}".encode('utf-8'))
                    partie_en_cours = vérifie_fin_de_partie(partie, fenetre, joueur_actuel.symbole)
                    if partie.tour_joueur == 1:
                        partie.tour_joueur = 2
                    else:
                        partie.tour_joueur = 1
                    print("sent")

                else:
                    print(partie.tour_joueur, tour_joueur)
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    if menu_pause.main():
                        return
                    else:
                        fenetre = pygame.display.set_mode((largeur_fenetre, hauteur_fenetre))
        affiche_trucs_de_base(fenetre, partie)

        if partie_en_cours:
            if joueur_actuel.symbole == "X":
                pygame.draw.rect(fenetre, (0, 0, 0), (largeur_fenetre - 100, 50, 50, 50), 5)
            else:
                #draw a circle top right corner
                pygame.draw.circle(fenetre, (0, 0, 0), (largeur_fenetre - 100, 50), 20, 5)
            pygame.display.flip()
        clock.tick(60)
        if partie.tour_joueur != tour_joueur and partie_en_cours:
            try:
                réponse = socket_client.recv(2048).decode('utf-8')
                print("received")
                if réponse.startswith("@jouer:"):
                    réponse = réponse.split(":")[1]
                    coup_str = réponse.split("|")
                    coup = int(coup_str[0]), int(coup_str[1])
                    print(coup)
                    partie.jouer(coup, partie.tour_joueur)
                    partie_en_cours = vérifie_fin_de_partie(partie, fenetre, joueur_actuel.symbole)
                    if not partie_en_cours:
                        return
                    if partie.tour_joueur == 1:
                        partie.tour_joueur = 2
                    else:
                        partie.tour_joueur = 1
            except BlockingIOError:
                pass
