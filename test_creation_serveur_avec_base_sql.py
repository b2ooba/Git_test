# Création d'un socket serveur TCP IPv4
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
IP, port = "127.0.0.1", 6666  # Adresse IP du serveur et le port d'écoute
server.bind((IP, port))      # Associe le socket à l'adresse et au port spécifiés
server.listen(10)              # Met le serveur en mode écoute pour jusqu'à 10 connexions entrantes

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

clients = []
pseudos = []

# Diffusion des messages
def diffuser(message):
    for client in clients:
        client.send(bytes(message, "utf-8"))

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

        # Vérifier si le pseudo existe déjà
        cursor.execute("SELECT * FROM utilisateurs WHERE pseudo=?", (pseudo,))
        utilisateur_existe = cursor.fetchone() is not None

        if utilisateur_existe:
            client.send(bytes("Ce pseudo est déjà pris. Veuillez choisir un autre pseudo.", "utf-8"))
            client.close()
            continue

        # Demander et vérifier les mots de passe
        mot_de_passe = client.recv(1024).decode("utf-8")
        client.send(bytes("Confirmez votre mot de passe : ", "utf-8"))
        confirmation_mot_de_passe = client.recv(1024).decode("utf-8")

        if mot_de_passe != confirmation_mot_de_passe:
            client.send(bytes("Les mots de passe ne correspondent pas. Fermeture de la connexion.", "utf-8"))
            client.close()
            continue

        ajouter_utilisateur_db(pseudo, mot_de_passe)
        ajouter_client_db(pseudo, adresse[0], adresse[1])

        clients.append(client)
        pseudos.append(pseudo)
        print(f"{pseudo} a rejoint le chat")
        client.send(bytes("Bienvenue dans le chat !\n", "utf-8"))

        # Page de connexion
        client.send(bytes("Entrez votre pseudo pour vous connecter : ", "utf-8"))
        pseudo_connexion = client.recv(1024).decode("utf-8")

        # Vérifier l'authentification de l'utilisateur
        mot_de_passe_connexion = client.recv(1024).decode("utf-8")
        if not verifier_authentification(pseudo_connexion, mot_de_passe_connexion):
            print(f"Tentative de connexion non autorisée pour {pseudo_connexion}")
            client.send(bytes("Erreur d'authentification. Veuillez créer un compte avant de vous connecter.", "utf-8"))
            client.close()
            continue

        # Récupérer tous les messages entre
