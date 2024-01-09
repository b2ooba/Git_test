import socket
import threading

# Création d'un socket serveur TCP IPv4
serveur = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
IP, port = "127.0.0.1", 6666
serveur.bind((IP, port))
serveur.listen(10)
clients = []
pseudos = {}

def diffuser(message, expeditaire=None, destinataire=None):
    for client, pseudo in pseudos.items():
        if destinataire is None or pseudo == destinataire:
            if client != expeditaire:
                client.send(bytes(message, "utf-8"))

def gestion_connexions():
    while True:
        client, adresse = serveur.accept()
        print(f"Connexion établie avec {str(adresse)}")
        pseudo = client.recv(1024).decode("utf-8")
        clients.append(client)
        pseudos[client] = pseudo
        print(f"{pseudo} a rejoint le chat")
        client.send(bytes("Bienvenue dans le chat !\n", "utf-8"))
        diffuser(f"{pseudo} a rejoint le chat!", destinataire=pseudo)
        thread_client = threading.Thread(target=gestion_client, args=(client, pseudo))
        thread_client.start()

def gestion_client(client, pseudo):
    while True:
        try:
            message = client.recv(1024).decode("utf-8")
            if message.startswith("@"):
                destinataire, message_prive = message.split(" ", 1)
                destinataire = destinataire[1:]
                diffuser(f"(Privé) {pseudo}: {message_prive}", expeditaire=client, destinataire=destinataire)
            elif message == "ecrit":
                clients.remove(client)
                client.close()
                del pseudos[client]
                diffuser(f"{pseudo} a quitté le chat!")
                break
            else:
                diffuser(f"{pseudo}: {message}")
        except:
            clients.remove(client)
            client.close()
            del pseudos[client]
            diffuser(f"{pseudo} a quitté le chat!")
            break

gestion_connexions()
print("Le serveur de chat est en marche")