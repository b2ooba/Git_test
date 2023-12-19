import socket
import select
import psycopg2

# Connexion à la base de données PostgreSQL
conn = psycopg2.connect(
    database="messagerie_db",
    user="votre_utilisateur",
    password="votre_mot_de_passe",
    host="127.0.0.1",
    port="6666"
)

# Création d'un curseur pour exécuter des requêtes SQL
cursor = conn.cursor()

# Création d'un socket serveur TCP IPv4
serveur = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
host, port = "127.0.0.1", 6666  # Adresse IP du serveur et le port d'écoute
serveur.bind((host, port))      # Associe le socket à l'adresse et au port spécifiés
serveur.listen(50)              # Met le serveur en mode écoute pour jusqu'à 50 connexions entrantes
client_connecte = True          # Indicateur de connexion client
socket_objs = [serveur]         # Liste des sockets à surveiller

print("Bienvenue dans la conversation !!!")

# Boucle principale du serveur
while client_connecte:
    # Sélection des sockets prêts à être lus
    liste_lue, liste_access_ecrit, exception = select.select(socket_objs, [], socket_objs)

    # Parcours des sockets prêts à être lus
    for socket_obj in liste_lue:

        # Nouvelle connexion entrante
        if socket_obj is serveur:
            client, adresse = serveur.accept()  # Accepte la connexion du client
            print(f"Objet client socket: {client} - adresse: {adresse}")
            socket_objs.append(client)  # Ajoute le socket du client à la liste des sockets à surveiller

        # Données reçues d'un client
        else:
            donnee_recue = socket_obj.recv(128).decode("utf-8")  # Reçoit des données du client

            if donnee_recue:
                print(donnee_recue)  # Affiche les données reçues

                # Exemple d'insertion dans la base de données
                cursor.execute("INSERT INTO messages (contenu, expediteur, destinataire) VALUES (%s, %s, %s)",
                               (donnee_recue, "expediteur_par_defaut", "destinataire_par_defaut"))
                conn.commit()

            # Le client s'est déconnecté
            else:
                socket_objs.remove(socket_obj)  # Retire le socket du client de la liste des sockets surveillés
                print("Un participant est déconnecté")
                print(f"{len(socket_objs) - 1} participants restants")

# Fermeture propre de la connexion à la base de données
cursor.close()
conn.close()
###test###
