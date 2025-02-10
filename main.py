import socket

def principal(ip_serveur):
    socket_client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    socket_client.connect((ip_serveur, 5555))
    print("Connecté au serveur")

    while True:
        reponse = socket_client.recv(1024).decode()
        if not reponse:
            break
        print(reponse, end="")

        if "entrez votre coup" in reponse or "Voulez-vous rejouer ?" in reponse or "Voulez-vous jouer vous-même ou laisser un bot jouer ?" in reponse:
            entree_utilisateur = input()
            socket_client.send(entree_utilisateur.encode())

    socket_client.close()

if __name__ == "__main__":
    principal('localhost')
