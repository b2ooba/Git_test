import socket  # Importe le module de gestion des sockets

# Création d'un socket serveur TCP IPv4
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
host, port = "127.0.0.1", 6666  # Adresse IP du serveur et le port d'écoute
client_socket.connect((host, port))
nom = input("Quelle est votre nom ?")

if __name__ == "__main__":

    while True:
        message = input(f"{nom} > ")
        client_socket.send(f"{nom} > {message}".encode("utf-8"))