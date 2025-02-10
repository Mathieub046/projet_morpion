#!/usr/bin/python3

import random
import time
import socket
from threading import Thread
from grid import *

def gerer_joueur(socket_client, joueur, grilles, tour, socket_adversaire, scores, grille_mise_a_jour, observateurs, socket_observateur=None):
    # Envoie des instructions et l'état de la grille au joueur
    socket_client.send("Voulez-vous jouer vous-même ou laisser un bot jouer ? (tapez 'moi' ou 'bot'): ".encode())
    choix_joueur = socket_client.recv(1024).decode().strip().lower()
    
    est_bot = (choix_joueur == 'bot')
    print(f"Le joueur {joueur} a choisi de jouer contre un {'bot' if est_bot else 'autre joueur'}")

    while True:
        # Envoi de l'état de la grille au joueur
        socket_client.send(f"Bienvenue Joueur {joueur}\n".encode())
        socket_client.send(grilles[joueur].afficher_chaine().encode())

        while grilles[0].partie_terminee() == -1:
            if tour[0] == joueur:
                socket_client.send("C'est votre tour !\n".encode())
                
                if est_bot:
                    coup = random.choice([i for i, cellule in enumerate(grilles[0].cellules) if cellule == VIDE])
                    socket_client.send(f"Le bot a joué le coup {coup}\n".encode())
                    
                    grilles[joueur].cellules[coup] = joueur
                    grilles[0].jouer(joueur, coup)
                    grille_mise_a_jour[0] = True
                    socket_client.send(grilles[joueur].afficher_chaine().encode())
                    tour[0] = JOUEUR2 if joueur == JOUEUR1 else JOUEUR1
                else:
                    coup = -1
                    while coup < 0 or coup >= NB_CELLES:
                        socket_client.send(f"Joueur {joueur}, entrez votre coup (0-8): ".encode())
                        try:
                            coup = int(socket_client.recv(1024).decode().strip())
                        except:
                            socket_client.send("Erreur: Entrez un nombre entre [0-8]\n".encode())
                            coup = -1
                    if grilles[0].cellules[coup] != VIDE:
                        grilles[joueur].cellules[coup] = grilles[0].cellules[coup]
                        socket_client.send("Cellule déjà prise, réessayez.\n".encode())
                        socket_client.send(grilles[joueur].afficher_chaine().encode())
                        coup = -1
                    else:
                        grilles[joueur].cellules[coup] = joueur
                        grilles[0].jouer(joueur, coup)
                        grille_mise_a_jour[0] = True
                        socket_client.send(grilles[joueur].afficher_chaine().encode())
                        tour[0] = JOUEUR2 if joueur == JOUEUR1 else JOUEUR1               
            else:
                socket_client.send("En attente de l'autre joueur...\n".encode())
            
            while tour[0] != joueur:
                time.sleep(1)

        socket_client.send("Partie terminée\n".encode())
        socket_client.send(grilles[0].afficher_chaine().encode())
        socket_adversaire.send("Partie terminée\n".encode())
        socket_adversaire.send(grilles[0].afficher_chaine().encode())

        if observateurs:
            for obs in observateurs:
                obs.send("Partie terminée\n".encode())
                obs.send(grilles[0].afficher_chaine().encode())

        if grilles[0].partie_terminee() == joueur:
            socket_client.send("Vous avez gagné !\n".encode())
            socket_adversaire.send("Vous avez perdu !\n".encode())
            scores[joueur - 1] += 1
        elif grilles[0].partie_terminee() == (JOUEUR2 if joueur == JOUEUR1 else JOUEUR1):
            socket_client.send("Vous avez perdu !\n".encode())
            socket_adversaire.send("Vous avez gagné !\n".encode())
            scores[(JOUEUR2 if joueur == JOUEUR1 else JOUEUR1) - 1] += 1
        else:
            socket_client.send("Égalité !\n".encode())
            socket_adversaire.send("Égalité !\n".encode())

        socket_client.send(f"Score actuel - Joueur 1: {scores[0]}, Joueur 2: {scores[1]}\n".encode())
        socket_adversaire.send(f"Score actuel - Joueur 1: {scores[0]}, Joueur 2: {scores[1]}\n".encode())
        if observateurs:
            for obs in observateurs:
                obs.send(f"Score actuel - Joueur 1: {scores[0]}, Joueur 2: {scores[1]}\n".encode())

        socket_client.send("Voulez-vous rejouer ? (oui/non): ".encode())
        socket_adversaire.send("Voulez-vous rejouer ? (oui/non): ".encode())
        reponse_joueur = socket_client.recv(1024).decode().strip().lower()
        reponse_adversaire = socket_adversaire.recv(1024).decode().strip().lower()

        if reponse_joueur != "oui" or reponse_adversaire != "oui":
            socket_client.send("Merci d'avoir joué !\n".encode())
            socket_adversaire.send("Merci d'avoir joué !\n".encode())
            if observateurs:
                for obs in observateurs:
                    obs.send("Les joueurs ont terminé la partie. Merci d'avoir observé !\n".encode())
            break

        grilles[0] = grid()
        grilles[joueur] = grid()
        grilles[JOUEUR2 if joueur == JOUEUR1 else JOUEUR1] = grid()

    socket_client.close()
    socket_adversaire.close()
    if observateurs:
        for obs in observateurs:
            obs.close()

def gerer_observateur(socket_observateur, grilles, grille_mise_a_jour, observateurs):
    try:
        socket_observateur.send("Connecté en tant qu'observateur. Vous verrez tous les coups.\n".encode())
        observateurs.append(socket_observateur)
        while True:
            if grille_mise_a_jour[0]:
                for obs in observateurs:
                    obs.send(grilles[0].afficher_chaine().encode())
                grille_mise_a_jour[0] = False
            time.sleep(0.5)
    except:
        observateurs.remove(socket_observateur)
        socket_observateur.close()
        print("Un observateur déconnecté")

def main():
    socket_serveur = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    socket_serveur.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    socket_serveur.bind(('localhost', 5555))
    socket_serveur.listen(3)
    print("Serveur en écoute sur le port 5555")

    grilles = [grid(), grid(), grid()]
    tour = [JOUEUR1]
    scores = [0, 0]
    grille_mise_a_jour = [False]
    observateurs = []

    socket_joueur1, _ = socket_serveur.accept()
    print("Joueur 1 connecté")
    socket_joueur2, _ = socket_serveur.accept()
    print("Joueur 2 connecté")

    Thread(target=gerer_joueur, args=(socket_joueur1, JOUEUR1, grilles, tour, socket_joueur2, scores, grille_mise_a_jour, observateurs)).start()
    Thread(target=gerer_joueur, args=(socket_joueur2, JOUEUR2, grilles, tour, socket_joueur1, scores, grille_mise_a_jour, observateurs)).start()

    try:
        while True:
            socket_observateur, _ = socket_serveur.accept()
            print("Observateur connecté")
            Thread(target=gerer_observateur, args=(socket_observateur, grilles, grille_mise_a_jour, observateurs)).start()
    except:
        print("Aucun autre observateur connecté")

if __name__ == "__main__":
    main()
