import threading
import socket

class Client:
    def __init__(self, server_ip = "127.0.0.1", port=6666):
        #Initialisation du socket serveur     
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        #connection au serveur
        self.connect_to_server(server_ip, port)
        #état du client (actif ou non)
        self.running = True
    
    def connect_to_server(self, ip, port):
        try:
            print("Connection en cours (°_°)")
            #connection au serveur
            self.server_socket.connect((ip,port))
            #Demande de pseudo au client
            pseudo = input("entrez votre pseudo: ")
            self.pseudo = pseudo
            # Envoie du pseudo au serveur
            self.server_socket.send(bytes(pseudo,"utf-8"))
            #Création du mot de passe au client
            mot_de_passe = input("Entrez votre mot de passe: ")
            # Envoie du mot de passe au serveur
            self.server_socket.send(bytes(mot_de_passe,"utf-8"))
            # Réception du message de bienvenu quand la connexion au serveur est réussi
            message_bienvenue = self.server_socket.recv(4096).decode('utf-8')
            print(message_bienvenue)
            self.création_compte()
        except Exception as e: # montre le message d'erreur pour la connexion au serveur (si il y en a)
            print("Erreur la connexion au serveur a echouée : ", str(e))

    def création_compte(self):
        """Permet à l'utilisateur de créer un compte"""
        pseudo = input("Entrer le pseudo que vous souhaitez utiliser: ")
        password = input("Entrer votre mot de passe: ")
        confirmation_mot_de_passe = input("Confirmez votre mot de passe: ")
        if password == confirmation_mot_de_passe:
            self.server_socket.send(bytes(f"CREATEACCOUNT {pseudo}:{password}", "utf-8"))
            reponse = self.server_socket.recv(4096).decode('utf-8').split("\n")[0]
            if reponse == "OK":
                print("Compte créé avec succès.")
                self.login()
            else:
                print("Erreur lors de la création du compte.")
        else:
             print("Les mots de passe ne correspondent pas.")



    def envoie_mesg(self):
        #Boucle pour envoyer des messages tant que le client et connectée  au serveur
        while self.running:
            #création du message souhaitée
            msg = input(f"{self.pseudo}> ")
            self.msg = msg
            #Envoi du message au serveur
            self.server_socket.send(f"{self.pseudo} > {msg}".encode("utf-8"))
            # Si le message est exit, le client se déconnecte
            if msg == "/exit":
                print("Déconnection en cours.....")
                break
            #if msg == "/new": # Si le message est new, une nouvelle discussion est créé.
                # nouvelle_discussion = msg.split("", 1) # 
                #self.server_socket.send(f"/new {nouvelle_discussion}".encode("utf-8"))
                #print(f"VOus avez crée une nouvelle discussion'{nouvelle_discussion}'.")
            #else: #
                #self.server_socket.send(f"{self.pseudo}>{msg}".encode("utf-8"))
                
    def recevoir_msg (self):
        #Boucle pour recevoir des messages tant que le client est connectée au serveur
        while True:
            try:
                #Réception des données depuis le serveur
                self.msg = self.server_socket.recv(1024).decode('utf-8')
                # Vérification si les donnéees ne sont pas vides
                if not self.msg:
                    print("erreur")
                    self.running = False
                    break
                else: 
                    print(self.msg)
            except Exception as e :
                print("erreur :", str(e))
                self.running = False
                break
    def start_threads (self):
        # Création des threads pour gérer l'envoi et la réception de messages simultanée
        reception_msg = threading.Thread(target=self.recevoir_msg)
        envoyee_msg = threading.Thread(target=self.envoie_mesg)
        # Démarrée les threads
        reception_msg.start()
        envoyee_msg.start()        
client = Client()
client.start_threads()
#fd