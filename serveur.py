<<<<<<< HEAD
import socket  # Importe le module de gestion des sockets
import select  # Importe le module Tkinter pour afficher des boîtes de dialogue
=======
import socket  # Importer le module de gestion des sockets
import threading  # Importer le module threading pour les threade
>>>>>>> 44c3d2bf45ccbcb55b2ec8c93e6afe3ba115c6e5

# Création d'un socket serveur TCP IPv4
serveur = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
host, port = "127.0.0.1", 6666  # Adresse IP du serveur et le port d'écoute
serveur.bind((host, port))      # Associe le socket à l'adresse et au port spécifiés
serveur.listen(50)              # Met le serveur en mode écoute pour jusqu'à 50 connexions entrantes
client_connectee = True         # Indicateur de connexion client.
socket_objs = [serveur]         # Liste des sockets à surveiller

print("Bienvenu dans la conversation !!!")

<<<<<<< HEAD
# Boucle principale du serveur
while client_connectee:
    # Sélection des sockets prêts à être lus
    liste_Lu , liste_access_Ecrit, exception = select.select(socket_objs, [], socket_objs)
    
    # Parcours des sockets prêts à être lus
    for socket_obj in liste_Lu:
        
        # Nouvelle connexion entrante 
        if socket_obj is serveur:
            client, adresse = serveur.accept()  # Accepte la connexion du client
            print(f"l'object client socket: {client} - adress: {adresse}")
            socket_objs.append(client)  # Ajoute le socket du client à la liste des sockets à surveiller
        
        # Données reçues d'un client  
        else:
            donnee_reçus = socket_obj.recv(1024).decode("utf-8")  # Reçoit des données du client

            if donnee_reçus:
                print(donnee_reçus)  # Affiche les données reçues
            # Le client s'est déconnecté
            else:
                socket_objs.remove(socket_obj)  # Retire le socket du client de la liste des sockets surveillés
                print("Un participant est déconnecté")
                print(f"{len(socket_objs) - 1} participants restant")
=======

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
               
    
>>>>>>> 44c3d2bf45ccbcb55b2ec8c93e6afe3ba115c6e5
