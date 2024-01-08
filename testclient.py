import threading
import socket

class Client:
    def __init__(self, server_ip="127.0.0.1", port=6666):
        # Initialisation du socket client
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # État du client (actif ou non)
        self.running = True
        # Connection au serveur
        self.connect_to_server(server_ip, port)

    def connect_to_server(self, ip, port):
        try:
            print("Connection en cours (°_°)")
            # Connection au serveur
            self.server_socket.connect((ip, port))
            # Demande de pseudo au client
            pseudo = input("Entrez votre pseudo: ")
            self.pseudo = pseudo
            # Envoi du pseudo au serveur
            self.server_socket.send(bytes(pseudo, "utf-8"))
            # Création du mot de passe au client
            mot_de_passe = input("Entrez votre mot de passe: ")
            # Envoi du mot de passe au serveur
            self.server_socket.send(bytes(mot_de_passe, "utf-8"))
            # Réception du message de bienvenue quand la connexion au serveur est réussie
            message_bienvenue = self.server_socket.recv(4096).decode('utf-8')
            print(message_bienvenue)
            # Appel à la fonction création_compte
            self.creation_compte()
        except Exception as e:  # Montre le message d'erreur pour la connexion au serveur (s'il y en a)
            print("Erreur la connexion au serveur a échoué : ", str(e))

    def creation_compte(self):
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
        # Boucle pour envoyer des messages tant que le client est connecté au serveur
        while self.running:
            # Création du message souhaité
            msg = input(f"{self.pseudo}> ")
            self.msg = msg
            # Envoi du message au serveur
            self.server_socket.send(f"{self.pseudo} > {msg}".encode("utf-8"))
            # Si le message est "/exit", le client se déconnecte
            if msg == "/exit":
                print("Déconnection en cours.....")
                break

    def recevoir_msg(self):
        # Boucle pour recevoir des messages tant que le client est connecté au serveur
        while True:
            try:
                # Réception des données depuis le serveur
                self.msg = self.server_socket.recv(1024).decode('utf-8')
                # Vérification si les données ne sont pas vides
                if not self.msg:
                    print("Erreur")
                    self.running = False
                    break
                else:
                    print(self.msg)
            except Exception as e:
                print("Erreur :", str(e))
                self.running = False
                break

    def start_threads(self):
        # Création des threads pour gérer l'envoi et la réception de messages simultanée
        reception_msg = threading.Thread(target=self.recevoir_msg)
        envoyee_msg = threading.Thread(target=self.envoie_mesg)
        # Démarrage des threads
        reception_msg.start()
        envoyee_msg.start()

client = Client()
client.start_threads()
