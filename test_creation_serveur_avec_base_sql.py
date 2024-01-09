import socket
import threading
import sqlite3
from flask import Flask

app = Flask(__name__)

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
IP, port = "127.0.0.1", 6666
server.bind((IP, port))
server.listen(10)
clients = {}
lock = threading.Lock()

def send_private_message(sender, receiver, message):
    if receiver in clients:
        receiver_client = clients[receiver]
        sender.send(bytes(f"Message privé pour {receiver}: {message}", "utf-8"))
        receiver_client.send(bytes(f"Message privé de {sender}: {message}", "utf-8"))
    else:
        sender.send(bytes(f"Erreur: {receiver} n'est pas connecté ou n'existe pas.", "utf-8"))

def broadcast(message, sender=None):
    with lock:
        for client in clients.values():
            if client != sender:
                client.send(bytes(message, "utf-8"))

def client_handler(client, pseudo):
    while True:
        try:
            message = client.recv(1024).decode("utf-8")
            if message == "/exit":
                with lock:
                    clients.pop(pseudo)
                client.close()
                broadcast(f"{pseudo} a quitté le chat!")
                break
            elif message.startswith("@"):
                parts = message.split(" ", 1)
                if len(parts) == 2:
                    send_private_message(pseudo, parts[0][1:], parts[1])
                else:
                    client.send(bytes("Format incorrect pour le message privé. Utilisez @destinataire message", "utf-8"))
            else:
                broadcast(f"{pseudo}: {message}", client)
        except:
            with lock:
                clients.pop(pseudo)
            client.close()
            broadcast(f"{pseudo} a quitté le chat!")
            break

def handle_connections():
    while True:
        client, address = server.accept()
        print(f"Connexion établie avec {str(address)}")

        client.send(bytes("Bienvenue ! Veuillez créer un compte ou vous connecter.\nEntrez votre pseudo : ", "utf-8"))
        pseudo = client.recv(1024).decode("utf-8").strip()

        with lock:
            if pseudo in clients:
                client.send(bytes("Ce pseudo est déjà pris. Veuillez choisir un autre pseudo.", "utf-8"))
                client.close()
            else:
                client.send(bytes("Entrez votre mot de passe : ", "utf-8"))
                mdp = client.recv(1024).decode("utf-8").strip()

                # Connexion à la base de données SQLite
                conn = sqlite3.connect('chat_database.db')
                cursor = conn.cursor()

                cursor.execute("SELECT * FROM clients WHERE pseudo=?", (pseudo,))
                existing_user = cursor.fetchone()

                if existing_user:
                    cursor.execute("SELECT * FROM clients WHERE pseudo=? AND mdp=?", (pseudo, mdp))
                    auth_successful = cursor.fetchone()

                    if auth_successful:
                        client.send(bytes(f"Bienvenue dans le chat, {pseudo}!\n", "utf-8"))
                        clients[pseudo] = client
                        threading.Thread(target=client_handler, args=(client, pseudo)).start()
                    else:
                        client.send(bytes("Erreur d'authentification. Fermeture de la connexion.", "utf-8"))
                        client.close()
                else:
                    cursor.execute("INSERT INTO clients (pseudo, mdp) VALUES (?, ?)", (pseudo, mdp))
                    conn.commit()
                    client.send(bytes(f"Compte créé avec succès. Bienvenue, {pseudo}!\n", "utf-8"))
                    clients[pseudo] = client
                    threading.Thread(target=client_handler, args=(client, pseudo)).start()

if __name__ == "__main__":
    threading.Thread(target=handle_connections).start()
    threading.Thread(target=app.run).start()
