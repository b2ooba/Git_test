import socket
import threading

# Paramètres du serveur
HOST = '127.0.0.1'
PORT = 55555

# Création du socket
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind((HOST, PORT))
server_socket.listen()

# Liste pour stocker les connexions des clients
clients = []

# Fonction pour gérer les messages des clients
def handle_client(client_socket):
    while True:
        try:
            # Attendre un message du client
            message = client_socket.recv(1024).decode('utf-8')
            if not message:
                # Si le message est vide, le client est déconnecté
                break

            # Diffuser le message à tous les autres clients
            for c in clients:
                c.send(message.encode('utf-8'))

        except:
            # En cas d'erreur, déconnecter le client
            index = clients.index(client_socket)
            clients.remove(client_socket)
            client_socket.close()
            break

# Fonction pour démarrer le serveur
def start_server():
    while True:
        # Attendre une nouvelle connexion
        client_socket, addr = server_socket.accept()
        clients.append(client_socket)

        # Démarrer un thread pour gérer le client
        client_thread = threading.Thread(target=handle_client, args=(client_socket,))
        client_thread.start()

# Démarrer le serveur
print(f"Serveur en écoute sur {HOST}:{PORT}")
start_server()
