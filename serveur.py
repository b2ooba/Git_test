import socket  # Importe le module de gestion des sockets
import select  # Importe le module Tkinter pour afficher des boîtes de dialogue
import socket  # Importer le module de gestion des sockets
import threading  # Importer le module threading pour les threade


# Création d'un socket serveur TCP IPv4
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
IP, port = "127.0.0.1", 6666  # Adresse IP du serveur et le port d'écoute
server.bind((IP, port))      # Associe le socket à l'adresse et au port spécifiés
server.listen(10)              # Met le serveur en mode écoute pour jusqu'à 10 connexions entrantes
clients =[]
pseudos = []

#diffusion des messages 
def diffuser(message):
    for client in clients:
        client.send(bytes(message, "utf-8"))


def gestion_connexions():
    while True:
        client, adresse = server.accept() 
        print(f"connexion établie avec {str(adresse)}")
        pseudo = client.recv(1024).decode("utf-8")
        clients.append(client)
        pseudos.append(pseudo)
        print(f"(pseudo) a réjoint le chat")
        client.send(bytes("Bienvenue dans le chat ! \n", "utf-8"))
        diffuser(f"{pseudo} a réjoint le chat!")
        thread_client = threading.Thread(target=gestion_client, args=(client, pseudo))
        thread_client.start()

def gestion_client(client, pseudo):
    while True:
        try:
            message = client.recv(1024).decode("utf-8")
            if message == "ecrit":
                index = clients.index(client)
                clients.remove(client)
                client.close()
                pseudo = pseudos[index]
                pseudos.remove(pseudo)
                diffuser(f"{pseudo} a quitté le chat !")
                break
            else:
                diffuser(f"{pseudo}: {message}")
        except:
            index = clients.index(client)
            clients.remove(client)
            client.close()
            pseudo = pseudos[index]
            pseudos.remove(pseudo)
            diffuser(f"{pseudo} a quitté le chat !")
            break

gestion_connexions()
print("Le serveur de chat est en marche")
