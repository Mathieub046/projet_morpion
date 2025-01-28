#!/usr/bin/python3

import sys
import socket

def main():
    # Connexion au serveur
    hostname_serveur = sys.argv[1]  # L'adresse du serveur passée en argument
    port_serveur = 2910
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect((hostname_serveur, port_serveur))
    
    player = 1  # Le joueur est numéroté (1 ou 2)
    
    while True:
        # Recevoir l'état actuel du jeu (sous forme de texte)
        data = client.recv(1024).decode()
        print(f"État du jeu: {data}")
        
        # Vérification si la partie est terminée
        if "a gagné" in data or "Match nul" in data:
            print(data)
            break
        
        # Demander au joueur de choisir une case
        shot = -1
        while shot < 0 or shot >= 9:
            shot = int(input(f"Joueur {player}, entrez votre coup (0-8): "))
        
        # Envoyer le coup au serveur
        client.send(str(shot).encode())
    
    client.close()

if __name__ == "__main__":
    main()
