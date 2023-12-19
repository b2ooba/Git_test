import socket  # Importe le module de gestion des sockets
import select  # Importe le module Tkinter pour afficher des boîtes de dialogue
import threading

# Création d'un socket serveur TCP IPv4
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
IP, port = "127.0.0.1", 6666  # Adresse IP du serveur et le port d'écoute
server.bind((IP, port))      # Associe le socket à l'adresse et au port spécifiés
server.listen(10)              # Met le serveur en mode écoute pour jusqu'à 10 connexions entrantes
clients =[]
pseudos = []

def diffuser(message):
    for client in clients:
        client.send(bytes(message, "utf-8"))


def gestion_de_connexion():
    while True:
        client, adresse = server.accept() 
        print(f"connexion établie avec {str(adresse)}")
        pseudo = client.recv(1024).decode("utf-8")
        clients.append(client)
        pseudos.append(pseudo)
        print(f"(pseudo) a réjoint le chat")
        client.send(bytes("Bienvenue dans le chat ! \n", "utf-8"))
        diffuser(f"{pseudo} a réjoint le chat !")
        thread.client = threading.Thread(target=gestion_client)



# client_connectee = True         # Indicateur de connexion client.
# socket_objs = [serveur]         # Liste des sockets à surveiller

# print("Bienvenu dans la conversation !!!")

# # Boucle principale du serveur
# while client_connectee:
#     # Sélection des sockets prêts à être lus
#     liste_Lu , liste_access_Ecrit, exception = select.select(socket_objs, [], socket_objs)
    
#     # Parcours des sockets prêts à être lus
#     for socket_obj in liste_Lu:
        
#         # Nouvelle connexion entrante 
#         if socket_obj is serveur:
#             client, adresse = serveur.accept()  # Accepte la connexion du client
#             print(f"l'object client socket: {client} - adress: {adresse}")
#             socket_objs.append(client)  # Ajoute le socket du client à la liste des sockets à surveiller
        
#         # Données reçues d'un client  
#         else:
#             donnee_reçus = socket_obj.recv(128).decode("utf-8")  # Reçoit des données du client

#             if donnee_reçus:
#                 print(donnee_reçus)  # Affiche les données reçues

#             # Le client s'est déconnecté
#             else:
#                 socket_objs.remove(socket_obj)  # Retire le socket du client de la liste des sockets surveillés
#                 print("Un participant est déconnecté")
#                 print(f"{len(socket_objs) - 1} participants restant")


# # Création d'un socket serveur TCP IPv4
# serveur = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# host, port = "127.0.0.1", 6666
# serveur.bind((host, port))
# serveur.listen(50)

# # Dictionnaire pour stocker les clients avec leurs identifiants
# clients = {}
# # Liste des sockets à surveiller
# socket_objs = [serveur]
# # Compteur pour générer des identifiants uniques
# id_counter = 1

# print("Bienvenue dans la conversation !!!")

# while True:
#     # Sélection des sockets prêts à être lus
#     liste_Lu, _, _ = select.select(socket_objs, [], socket_objs)

#     for socket_obj in liste_Lu:
#         # Nouvelle connexion entrante
#         if socket_obj is serveur:
#             client, adresse = serveur.accept()
#             print(f"Nouvelle connexion de {adresse}")

#             # Attribuer un identifiant unique au client
#             client_id = id_counter
#             id_counter += 1

#             socket_objs.append(client)
#             # Stocker les informations du client dans le dictionnaire
#             clients[client] = {"id": client_id, "username": None}
#             client.send(f"Bienvenue dans le chat! Votre identifiant est {client_id}. Entrez votre nom d'utilisateur:".encode("utf-8"))

#         # Données reçues d'un client
#         else:
#             donnee_reçus = socket_obj.recv(128).decode("utf-8")

#             if donnee_reçus:
#                 # Si le client n'a pas de nom d'utilisateur, utilisez-le comme nom d'utilisateur
#                 if clients[socket_obj]["username"] is None:
#                     clients[socket_obj]["username"] = donnee_reçus
#                     print(f"{donnee_reçus} a rejoint le chat avec l'identifiant {clients[socket_obj]['id']}.")
#                     socket_obj.send("Vous avez rejoint le chat.".encode("utf-8"))
#                 else:
#                     # Analyser le message et extraire le destinataire et le message
#                     parts = donnee_reçus.split(':', 2)
#                     if len(parts) == 3:
#                         sender = clients[socket_obj]["username"]
#                         dest_id, message = parts[0], parts[2]

#                         # Rechercher le destinataire dans le dictionnaire clients
#                         for dest_socket, dest_info in clients.items():
#                             if dest_info["id"] == int(dest_id):
#                                 dest_socket.send(f"{sender}: {message}".encode("utf-8"))
#                                 break
#                         else:
#                             socket_obj.send(f"Destinataire avec l'identifiant {dest_id} introuvable.".encode("utf-8"))
#             else:
#                 # Le client s'est déconnecté
#                 socket_objs.remove(socket_obj)
#                 client_info = clients.pop(socket_obj, None)
#                 if client_info:
#                     print(f"{client_info['username']} s'est déconnecté")

