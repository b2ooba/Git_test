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
def message(sender, receiver, message):
    if receiver in pseudos:
        receiver_client = pseudos[receiver]
        sender.send(bytes(f"Message privé pour {receiver}: {message}", "utf-8"))
        receiver_client.send(bytes(f"Message privé de {sender}: {message}", "utf-8"))
    else:
        sender.send(bytes(f"Erreur: {receiver} n'est pas connecté ou n'existe pas.", "utf-8"))

def diffuser(message, sender=None):
    for client in clients:
        if client != sender:
            client.send(bytes(message, "utf-8"))

def gestion_client(client, pseudo):
    while True:
        try:
            message = client.recv(1024).decode("utf-8")
            if message == "/exit":
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
                    message(pseudo, parts[0][1:], parts[1])
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

# Connexion à la base de données SQLite
conn = sqlite3.connect('chat_database.db')
cursor = conn.cursor()

# Création de la table 'utilisateurs' pour stocker les informations d'authentification
cursor.execute('''
    CREATE TABLE IF NOT EXISTS utilisateurs (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        pseudo TEXT UNIQUE,
        mot_de_passe TEXT
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

# Création de la table 'clients' pour stocker les informations de connexion
cursor.execute('''
    CREATE TABLE IF NOT EXISTS clients (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        pseudo TEXT,
        address TEXT,
        port INTEGER
    )
''')
conn.commit()

# Fonction pour ajouter un utilisateur à la base de données
def ajouter_utilisateur_db(pseudo, mot_de_passe):
    cursor.execute("INSERT INTO utilisateurs (pseudo, mot_de_passe) VALUES (?, ?)", (pseudo, mot_de_passe))
    conn.commit()

# Fonction pour vérifier les informations d'authentification d'un utilisateur
def verifier_authentification(pseudo, mot_de_passe):
    cursor.execute("SELECT * FROM utilisateurs WHERE pseudo=? AND mot_de_passe=?", (pseudo, mot_de_passe))
    return cursor.fetchone() is not None

# Fonction pour ajouter un client à la base de données
def ajouter_client_db(pseudo, address, port):
    cursor.execute("INSERT INTO clients (pseudo, address, port) VALUES (?, ?, ?)", (pseudo, address, port))
    conn.commit()

# Fonction pour stocker un message dans la base de données
def stocker_message_db(expediteur, destinataire, message):
    cursor.execute("INSERT INTO messages (expediteur, destinataire, message) VALUES (?, ?, ?)", (expediteur, destinataire, message))
    conn.commit()

# Fonction pour récupérer tous les messages entre deux utilisateurs
def recuperer_messages_db(expediteur, destinataire):
    cursor.execute("SELECT * FROM messages WHERE (expediteur=? AND destinataire=?) OR (expediteur=? AND destinataire=?) ORDER BY id", (expediteur, destinataire, destinataire, expediteur))
    return cursor.fetchall()
 
# Fonction pour gérer les connexions des clients
def gestion_connexions():
    while True:
        client, adresse = server.accept()
        print(f"Connexion établie avec {str(adresse)}")

        # Page de création de compte
        client.send(bytes("Bienvenue ! Veuillez créer un compte.\nEntrez votre pseudo : ", "utf-8"))
        pseudo = client.recv(1024).decode("utf-8")

        cursor.execute("SELECT * FROM utilisateurs WHERE pseudo=?", (pseudo,))
        utilisateur_existe = cursor.fetchone() is not None

        if utilisateur_existe:
            client.send(bytes("Ce pseudo est déjà pris. Veuillez choisir un autre pseudo.", "utf-8"))
            client.close()
            continue

        mot_de_passe = client.recv(1024).decode("utf-8")
        client.send(bytes("Confirmez votre mot de passe : ", "utf-8"))
        confirmation_mot_de_passe = client.recv(1024).decode("utf-8")

        if mot_de_passe != confirmation_mot_de_passe:
            client.send(bytes("Les mots de passe ne correspondent pas. Fermeture de la connexion.", "utf-8"))
            client.close()
            continue

        # Vérifier l'authentification de l'utilisateur avant de rejoindre le chat
        if verifier_authentification(pseudo, mot_de_passe):
            ajouter_client_db(pseudo, adresse[0], adresse[1])

            clients.append(client)
            pseudos[pseudo] = client
            print(f"{pseudo} a rejoint le chat")
            client.send(bytes("Bienvenue dans le chat !\n", "utf-8"))

            # Page de connexion
            client.send(bytes("Entrez votre pseudo pour vous connecter : ", "utf-8"))
            pseudo_connexion = client.recv(1024).decode("utf-8")

            mot_de_passe_connexion = client.recv(1024).decode("utf-8")
            if verifier_authentification(pseudo_connexion, mot_de_passe_connexion):
                print(f"{pseudo_connexion} s'est connecté.")
                client.send(bytes(f"Bienvenue {pseudo_connexion}!\n", "utf-8"))
                threading.Thread(target=gestion_client, args=(client, pseudo_connexion)).start()
            else:
                print(f"Tentative de connexion non autorisée pour {pseudo_connexion}")
                client.send(bytes("Erreur d'authentification. Veuillez créer un compte avant de vous connecter.", "utf-8"))
                client.close()
        else:
            client.send(bytes("Erreur d'authentification. Veuillez créer un compte avant de vous connecter.", "utf-8"))
            client.close()

# Lancer la gestion des connexions dans un thread séparé
threading.Thread(target=gestion_connexions).start()