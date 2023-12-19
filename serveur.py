import socket  # gestioon de socket 
import select  # gestion Tkinter pour afficher des boîtes de dialogue


serveur = socket.socket (socket.AF_INET, socket.SOCK_STREAM) 
host, port = "127.0.0.1", 6666  # Adresse IP du serveur et le port d'écoute
serveur.bind((host, port))      # Associe le socket à l'adresse et au port spécifiés
serveur.listen(50)              # Met le serveur en mode écoute pour jusqu'à 50 connexions entrantes
client_connectee = True         # Indicateur de connexion client.
socket_objs = [serveur]         # Liste des sockets à surveiller

print("Bienvenu dans la conversation !!!")

while client_connectee:
    liste_Lu , liste_access_Ecrit, exception = select.select(socket_objs, [], socket_objs)
    for socket_obj in liste_Lu:
        
        #Nouvelle connexion entrante 
        if socket_obj is serveur:
            client, adresse = serveur.accept()
            print(f"l'object client socket: {client} - adress: {adresse}")
            socket_objs.append(client)
        
        #Données réçus d'un client  
        else:
            donnee_reçus = socket_obj.recv(128).decode("utf-8")

            if donnee_reçus:
                print(donnee_reçus)

            #Le client s'est connectée
            else:
                socket_objs.remove(socket_obj)
                print("Un participant est déconnecté")
                print(f"{len(socket_objs) - 1} participants restant")




