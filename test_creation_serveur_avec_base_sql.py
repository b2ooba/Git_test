import socket
import threading
import sqlite3

# Création d'un socket serveur TCP IPv4
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
IP, port = "127.0.0.1", 6666
server.bind((IP, port))
server.listen(10)
clients = []
pseudos = {}

# Diffusion des messages privés
def send_private_message(sender, receiver, message):
    if receiver in pseudos:
        receiver_client = pseudos[receiver]
        sender.send(bytes(f"Message privé pour {receiver}: {message}", "utf-8"))
        receiver_client.send(bytes(f"Message privé de {sender}: {message}", "utf-8"))
    else:
        sender.send(bytes(f"Erreur: {receiver} n'est pas connecté ou n'existe pas.", "utf-8"))

def broadcast(message, sender=None):
    for client in clients:
        if client != sender:
            client.send(bytes(message, "utf-8"))

def client_handler(client, pseudo):
    while True:
        try:
            message = client.recv(1024).decode("utf-8")
            if message == "/exit":
                index = clients.index(client)
                clients.remove(client)
                pseudo = pseudos.pop(pseudo)
                client.close()
                broadcast(f"{pseudo} a quitté le chat!")
                break
            elif message.startswith("@"):
                # Format du message privé : @destinataire message
                parts = message.split(" ", 1)
                if len(parts) == 2:
                    send_private_message(pseudo, parts[0][1:], parts[1])
                else:
                    client.send(bytes("Format incorrect pour le message privé. Utilisez @destinataire message", "utf-8"))
            else:
                broadcast(f"{pseudo}: {message}", client)
        except:
            index = clients.index(client)
            clients.remove(client)
            pseudo = pseudos.pop(pseudo)
            client.close()
            broadcast(f"{pseudo} a quitté le chat!")
            break

# Connexion à la base de données SQLite
conn = sqlite3.connect('chat_database.db')
cursor = conn.cursor()

# Création de la table 'utilisateurs' pour stocker les informations d'authentification
cursor.execute('''
    CREATE TABLE IF NOT EXISTS utilisateurs (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        pseudo TEXT UNIQUE,
        mdp TEXT
    )
''')
conn.commit()

# Création de la table 'messages' pour stocker les messages
cursor.execute('''
    CREATE TABLE IF NOT EXISTS messages (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        expediteur TEXT,
        destinataire TEXT,
        message TEXT
    )
''')
conn.commit()

# Création de la table 'clients'
cursor.execute('''
    CREATE TABLE IF NOT EXISTS clients (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        pseudo TEXT UNIQUE,
        mdp TEXT
    )
''')
conn.commit()

# Fonction pour ajouter un client à la base de données
def add_client_to_db(pseudo, mdp, address, port):
    cursor.execute("INSERT INTO clients (pseudo, mdp) VALUES (?, ?)", (pseudo, mdp))
    conn.commit()

# Fonction pour vérifier les informations d'authentification d'un client
def verify_authentication(pseudo, mdp):
    cursor.execute("SELECT * FROM utilisateurs WHERE pseudo=? AND mdp=?", (pseudo, mdp))
    return cursor.fetchone() is not None

# Fonction pour stocker un message dans la base de données
def store_message_in_db(expediteur, destinataire, message):
    cursor.execute("INSERT INTO messages (expediteur, destinataire, message) VALUES (?, ?, ?)", (expediteur, destinataire, message))
    conn.commit()

# Fonction pour récupérer tous les messages entre deux utilisateurs
def retrieve_messages_from_db(expediteur, destinataire):
    cursor.execute("SELECT * FROM messages WHERE (expediteur=? AND destinataire=?) OR (expediteur=? AND destinataire=?) ORDER BY id", (expediteur, destinataire, destinataire, expediteur))
    return cursor.fetchall()

# Fonction pour gérer les connexions des clients
def handle_connections():
    local_conn = threading.local()
    local_conn.conn = sqlite3.connect('chat_database.db')
    local_conn.cursor = local_conn.conn.cursor()

    while True:
        client, adresse = server.accept()
        print(f"Connexion établie avec {str(adresse)}")

        # Page de création de compte
        client.send(bytes("Bienvenue ! Veuillez créer un compte.\nEntrez votre pseudo : ", "utf-8"))
        pseudo = client.recv(1024).decode("utf-8")
