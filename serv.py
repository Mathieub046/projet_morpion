# serv.py

import socket
from grid import *  # Importation de la classe grid

def get_masked_grid(grid, player, reveal_opponent=False):
    """Retourne une version de la grille masquée ou complète."""
    masked_cells = [
        cell if cell == player or cell == EMPTY or reveal_opponent else EMPTY
        for cell in grid.cells
    ]
    grid_state = "\n".join([
        " -------------",
        f" | {symbols[masked_cells[0]]} | {symbols[masked_cells[1]]} | {symbols[masked_cells[2]]} | ",
        " -------------",
        f" | {symbols[masked_cells[3]]} | {symbols[masked_cells[4]]} | {symbols[masked_cells[5]]} | ",
        " -------------",
        f" | {symbols[masked_cells[6]]} | {symbols[masked_cells[7]]} | {symbols[masked_cells[8]]} | ",
        " -------------"
    ])
    return grid_state

def main():
    # Création de la socket serveur
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    
    hostname = socket.gethostname()
    s.bind((socket.gethostbyname(hostname), 2910))  # Écoute sur le port 2910
    s.listen(2)  # Le serveur attend 2 clients
    
    print("Serveur en attente de connexions...")
    clients = []

    # Acceptation des connexions des deux joueurs
    while len(clients) < 2:
        client_socket, client_address = s.accept()
        clients.append(client_socket)
        print(f"Connexion acceptée de {client_address}")

    print("Les deux joueurs sont connectés. Le jeu commence !")
    
    while True:
        current_player = 0  # Joueur 1 commence
        game_grid = grid()  # Créer une nouvelle grille
        
        while True:
            player = current_player + 1  # Joueur courant (1 ou 2)
            client = clients[current_player]
            
            while True:  # Boucle pour s'assurer qu'un coup valide est joué
                # Envoyer la version appropriée de la grille
                masked_grid = get_masked_grid(game_grid, player, False)
                client.send(f"Votre tour !\n{masked_grid}".encode())
                
                # Recevoir le coup du joueur
                data = client.recv(1024).decode()
                if not data:
                    break
                
                # Traitement du coup
                shot = int(data.strip())
                if game_grid.cells[shot] == EMPTY:
                    # Jouer le coup si la case est vide
                    game_grid.play(player, shot)
                    break  # Sortir de la boucle car un coup valide a été joué
                else:
                    client.send(f"Cette case ({shot}) est déjà occupée !\n{masked_grid}".encode())

            # Vérifier la fin du jeu
            if game_grid.gameOver() != -1:
                # Le jeu est terminé
                result_message = ""
                if game_grid.gameOver() == 0:
                    result_message = "Match nul !"
                elif game_grid.gameOver() == player:
                    result_message = "Vous avez gagné !"
                else:
                    result_message = "Vous avez perdu !"
                
                # Informer les deux joueurs du résultat final
                for i, c in enumerate(clients):
                    final_grid = get_masked_grid(game_grid, i + 1, True)
                    if game_grid.gameOver() == i + 1:
                        c.send(f"{result_message}\nVoici la grille finale :\n{final_grid}".encode())
                    else:
                        c.send(f"Vous avez perdu !\nVoici la grille finale :\n{final_grid}".encode())

                # Demander si les joueurs veulent recommencer
                for c in clients:
                    c.send("Voulez-vous jouer une autre partie ? (oui/non)".encode())
                
                responses = [c.recv(1024).decode().strip().lower() for c in clients]
                if all(response == "oui" for response in responses):
                    # Réinitialiser la grille et continuer à jouer
                    game_grid.reset()
                    continue
                else:
                    break  # Quitter la boucle principale du jeu

            # Changer de joueur
            current_player = 1 - current_player  # Alterner entre joueur 1 et joueur 2

        # Si le serveur reçoit une demande de quitter, on arrête
        print("Une des parties est terminée, les joueurs ne veulent plus continuer.")
        break
    
    # Fermer les connexions
    for client in clients:
        client.close()

if __name__ == "__main__":
    main()
