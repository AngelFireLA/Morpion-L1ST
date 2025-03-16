import ipaddress
import os

import pygame
import json


def souris_est_dans_zone(souris, zone):
    x, y, largeur, hauteur = zone
    return x < souris[0] < x + largeur and y < souris[1] < y + hauteur


def afficher_texte(fenetre, x, y, texte, taille, couleur=(0, 0, 0), font="freesansbold.ttf"):
    font = pygame.font.Font(font, taille)
    texte = font.render(texte, True, couleur)
    text_rect = texte.get_rect(center=(x, y))
    fenetre.blit(texte, text_rect)


def charger_config():
    with open(chemin_absolu_dossier+"config.json", "r") as fichier:
        return json.load(fichier)


def récupérer_port():
    return charger_config()["port"]


def récupérer_ip_cible():
    return charger_config()["ip"]


def mettre_à_jour_ip(nouvelle_ip):
    config = charger_config()
    config["ip"] = nouvelle_ip
    with open(chemin_absolu_dossier+"config.json", "w") as fichier:
        json.dump(config, fichier)


def est_local():
    return charger_config()["local"]


def mettre_à_jour_port(nouveau_port):
    config = charger_config()
    config["port"] = nouveau_port
    with open(chemin_absolu_dossier+"config.json", "w") as fichier:
        json.dump(config, fichier)


def ip_est_valide(ip):
    try:
        ipaddress.IPv4Address(ip)
        return True
    except ValueError:
        return False


# liste de couleurs nom:rgb
dict_couleurs = {
    "rouge": (255, 0, 0),
    "vert": (0, 255, 0),
    "bleu": (0, 0, 255),
    "jaune": (255, 255, 0),
    "noir": (0, 0, 0),
    "blanc": (255, 255, 255),
    "gris": (128, 128, 128),
    "marron": (139, 69, 19),
    "rose": (255, 105, 180),
    "violet": (128, 0, 128),
    "cyan": (0, 255, 255),
    "orange": (255, 165, 0),
    "bleu marin": (20, 40, 70),
    "boutton": (255, 150, 113),
    "marron clair": (190, 118, 48),
}

largeur_fenetre, hauteur_fenetre = 800, 600
couleurs_cases = (dict_couleurs["blanc"], dict_couleurs["marron clair"])
serveur_tourne = False
chemin_absolu_dossier = os.path.dirname(os.path.abspath(__file__)) + "/"

def status_serveur(status=None):
    global serveur_tourne
    if status is None:
        return serveur_tourne
    serveur_tourne = status

def coups_légaux(grille):
    coups = []
    for y in range(3):
        for x in range(3):
            if not grille[y][x]:
                coups.append((x, y))
    return coups


def copier_grille(grille):
    return [[case for case in ligne] for ligne in grille]


def vérifier_si_victoire(grille):
    for i in range(3):
        if grille[i][0] == grille[i][1] == grille[i][2] and grille[i][0]:
            return (i, 0), (i, 2), grille[i][0]
        if grille[0][i] == grille[1][i] == grille[2][i] and grille[0][i]:
            return (0, i), (2, i), grille[0][i]
    if grille[0][0] == grille[1][1] == grille[2][2] and grille[0][0]:
        return (0, 0), (2, 2), grille[0][0]
    if grille[0][2] == grille[1][1] == grille[2][0] and grille[0][2]:
        return (0, 2), (2, 0), grille[0][2]
    return False


def vérifier_si_match_nul(grille):
    for ligne in grille:
        for case in ligne:
            if not case:
                return False
    return True

def symbole_opposé(symbole):
    return "O" if symbole == "X" else "X"
