# import socket  # Importe le module de gestion des sockets
# import select  # Importe le module Tkinter pour afficher des boîtes de dialogue

# # Création d'un socket serveur TCP IPv4
# serveur = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# host, port = "127.0.0.1", 6666  # Adresse IP du serveur et le port d'écoute
# serveur.bind((host, port))      # Associe le socket à l'adresse et au port spécifiés
# serveur.listen(50)              # Met le serveur en mode écoute pour jusqu'à 50 connexions entrantes
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


import socket
import select

serveur = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
host, port = "127.0.0.1", 6666
serveur.bind((host, port))
serveur.listen(50)
client_connectee = True
socket_objs = [serveur]
clients = {}  # Dictionnaire pour stocker les clients par leurs identifiants unique

print("Bienvenue dans la conversation !!!")

while client_connectee:
    liste_Lu, _, _ = select.select(socket_objs, [], socket_objs)

    for socket_obj in liste_Lu:
        # Nouvelle connexion entrante
        if socket_obj is serveur:
            client, adresse = serveur.accept()
            print(f"Nouvelle connexion de {adresse}")
            socket_objs.append(client)
            client.send("Bienvenue dans le chat! Entrez votre nom d'utilisateur:".encode("utf-8"))

        # Données reçues d'un client
        else:
            donnee_reçus = socket_obj.recv(128).decode("utf-8")

            if donnee_reçus:
                # Si l'utilisateur n'a pas d'identifiant, utilisez-le comme identifiant
                if socket_obj not in clients:
                    clients[socket_obj] = donnee_reçus
                    print(f"{donnee_reçus} a rejoint le chat.")
                    socket_obj.send("Vous avez rejoint le chat.".encode("utf-8"))
                else:
                    if ":" in donnee_reçus:
                        # Récupérez l'expéditeur du message
                        sender = clients[socket_obj]
                    
                        # Récupérez le destinataire et le message
                        destinataire, message = donnee_reçus.split(':', 1)
                    
                    # Recherchez le socket du destinataire dans le dictionnaire clients
                        for dest_socket, username in clients.items():
                            if username == destinataire:
                                dest_socket.send(f"{sender}: {message}".encode("utf-8"))
                                break
                        else:
                            socket_obj.send(f"Destinataire {destinataire} introuvable.".encode("utf-8"))
                    else:
                        socket_obj.send("Format de message incorrect. Utilisez 'destinataire:message'.".encode("utf-8"))
            else:
                # Le client s'est déconnecté
                socket_objs.remove(socket_obj)
                print(f"{clients.get(socket_obj, 'Un participant')} s'est déconnecté")
                clients.pop(socket_obj, None)

print("Fermeture du serveur.")
serveur.close()
