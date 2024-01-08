import socket
import select
import threading

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
IP, port = "127.0.0.1", 6666
server.bind((IP, port))
server.listen(10)
clients = []
pseudos = {}

def diffuser(message, sender=None):
    for client in clients:
        if client != sender:
            client.send(bytes(message, "utf-8"))

def envoyer_message_prive(sender, receiver, message):
    if receiver in pseudos:
        receiver_client = pseudos[receiver]
        sender.send(bytes(f"Message privé pour {receiver}: {message}", "utf-8"))
        receiver_client.send(bytes(f"Message privé de {sender}: {message}", "utf-8"))
    else:
        sender.send(bytes(f"Erreur: {receiver} n'est pas connecté ou n'existe pas.", "utf-8"))

def gestion_connexions():
    while True:
        client, adresse = server.accept()
        print(f"connexion établie avec {str(adresse)}")
        pseudo = client.recv(1024).decode("utf-8")
        clients.append(client)
        pseudos[pseudo] = client
        print(f"{pseudo} a rejoint le chat")
        client.send(bytes("Bienvenue dans le chat ! \n", "utf-8"))
        diffuser(f"{pseudo} a rejoint le chat!")
        thread_client = threading.Thread(target=gestion_client, args=(client, pseudo))
        thread_client.start()

def gestion_client(client, pseudo):
    while True:
        try:
            message = client.recv(1024).decode("utf-8")
            if message == "ecrit":
                index = clients.index(client)
                clients.remove(client)
                pseudo = pseudos.pop(pseudo)
                client.close()
                diffuser(f"{pseudo} a quitté le chat!")
                break
            elif message.startswith("@"):
                # Format du message privé : @destinataire message
                parts = message.split(" ", 1)
                if len(parts) == 2:
                    envoyer_message_prive(pseudo, parts[0][1:], parts[1])
                else:
                    client.send(bytes("Format incorrect pour le message privé. Utilisez @destinataire message", "utf-8"))
            else:
                diffuser(f"{pseudo}: {message}", client)
        except:
            index = clients.index(client)
            clients.remove(client)
            pseudo = pseudos.pop(pseudo)
            client.close()
            diffuser(f"{pseudo} a quitté le chat!")
            break

gestion_connexions()
print("Le serveur de chat est en marche")
