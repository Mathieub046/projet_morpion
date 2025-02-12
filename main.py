import socket
import sys

def main(server_ip):
    while True:
        try:
            client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            client_socket.connect((server_ip, 5555))
            print("Connected to the server")
            break
        except (socket.error, ConnectionRefusedError):
            print("Connection failed. Retrying in 5 seconds...")
            client_socket.close()
            continue
    
    while True:
        try:
            response = client_socket.recv(1024).decode()
            if not response:
                break
            print(response)
            
            if "Your turn!" in response:
                move = input("Enter your move: ")
                client_socket.send(move.encode())
        except (socket.error, ConnectionResetError):
            print("Connection lost. Trying to reconnect...")
            client_socket.close()
            main(server_ip)
            break
    
    client_socket.close()

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python client.py <server_ip>")
    else:
        main(sys.argv[1])
