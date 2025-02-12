import socket
import time
import random
from threading import Thread
from grid import *

def handle_client(client_socket, player, grids, turn, other_socket, scores, grid_updated, observers):
    """Gère un joueur, reçoit ses coups et met à jour la partie."""
    client_socket.send("Do you want to play yourself or let a bot play? (type 'me' or 'bot'): ".encode())
    player_choice = client_socket.recv(1024).decode().strip().lower()
    is_bot = (player_choice == 'bot')
    print(f"Player {player} chose {'bot' if is_bot else 'human'}")
    
    while True:
        client_socket.send(f"Welcome Player {player}\n".encode())
        client_socket.send(grids[player].display_string().encode())
        
        while grids[0].game_over() == -1:
            if turn[0] == player:
                client_socket.send("Your turn!\n".encode())
                
                if is_bot:
                    move = random.choice([i for i, cell in enumerate(grids[0].cells) if cell == EMPTY])
                    client_socket.send(f"Bot played move {move}\n".encode())
                    grids[player].cells[move] = player
                    grids[0].play(player, move)
                    grid_updated[0] = True
                else:
                    move = -1
                    while move < 0 or move >= NB_CELLS or grids[0].cells[move] != EMPTY:
                        client_socket.send("Enter your move (0-8): ".encode())
                        try:
                            move = int(client_socket.recv(1024).decode().strip())
                        except ValueError:
                            client_socket.send("Invalid input! Enter a number between 0-8.\n".encode())
                            continue
                    grids[player].cells[move] = player
                    grids[0].play(player, move)
                    grid_updated[0] = True
                    
                client_socket.send(grids[player].display_string().encode())
                turn[0] = J2 if player == J1 else J1
            else:
                client_socket.send("Waiting for the other player...\n".encode())
            
            while turn[0] != player:
                time.sleep(1)
        
        send_game_end(client_socket, other_socket, observers, grids, scores, player)
        
        client_socket.send("Do you want to play again? (yes/no): ".encode())
        other_socket.send("Do you want to play again? (yes/no): ".encode())
        response = client_socket.recv(1024).decode().strip().lower()
        other_response = other_socket.recv(1024).decode().strip().lower()
        
        if response != "yes" or other_response != "yes":
            client_socket.send("Thanks for playing!\n".encode())
            other_socket.send("Thanks for playing!\n".encode())
            for obs in observers:
                obs.send("Players have ended the game. Thanks for watching!\n".encode())
            break
        
        grids[0] = Grid()
        grids[J1] = Grid()
        grids[J2] = Grid()
    
    client_socket.close()
    other_socket.close()
    for obs in observers:
        obs.close()

def main():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_socket.bind(('localhost', 5555))
    server_socket.listen(3)
    print("Server listening on port 5555")
    
    grids = [Grid(), Grid(), Grid()]
    turn = [J1]
    scores = [0, 0]
    grid_updated = [False]
    observers = []
    
    client_socket1, _ = server_socket.accept()
    print("Connection from player 1")
    client_socket2, _ = server_socket.accept()
    print("Connection from player 2")
    
    Thread(target=handle_client, args=(client_socket1, J1, grids, turn, client_socket2, scores, grid_updated, observers)).start()
    Thread(target=handle_client, args=(client_socket2, J2, grids, turn, client_socket1, scores, grid_updated, observers)).start()
    
    try:
        while True:
            observer_socket, _ = server_socket.accept()
            print("Connection from observer")
            Thread(target=handle_observer, args=(observer_socket, grids, grid_updated, observers)).start()
    except:
        print("No observer connected")

if __name__ == "__main__":
    main()