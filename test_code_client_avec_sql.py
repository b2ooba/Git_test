import threading
import socket

class Client:
    def __init__(self, server_ip="127.0.0.1", port=6666):
        # Initialisation du socket serveur
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # Connection au serveur
        self.connect_to_server(server_ip, port)
        # État du client (actif ou non)
        self.running = True

    def connect_to_server(self, ip, port):
        try:
            print("Connection en cours (°_°)")
            # Connection au serveur
            self.server_socket.connect((ip, port))
            # Demande de pseudo au client
            pseudo = input("Entrez votre pseudo: ")
            # Envoie du pseudo au serveur
            self.server_socket.send(bytes(pseudo, "utf-8"))
            
            # Demande de mot de passe au client
            mot_de_passe = input("Entrez votre mot de passe: ")
            # Envoi du mot de passe au serveur
            self.server_socket.send(bytes(mot_de_passe, "utf-8"))
            
            # Réception du message du serveur après la connexion
            message_bienvenue = self.server_socket.recv(4096).decode('utf-8')
            print(message_bienvenue)

        except Exception as e:
            print("Erreur la connexion au serveur a échoué : ", str(e))

    def create_account(self):
        while True:
            # Demande de création de compte
            create_account_input = input("Vous n'avez pas de compte. Voulez-vous créer un compte? (oui/non): ").lower()

            if create_account_input == "oui":
                # Création d'un compte
                pseudo = input("Entrez un pseudo pour votre compte: ")
                mot_de_passe = input("Entrez un mot de passe: ")
                confirmation_mot_de_passe = input("Confirmez votre mot de passe: ")

                # Vérification que les mots de passe correspondent
                if mot_de_passe == confirmation_mot_de_passe:
                    self.server_socket.send(bytes("create_account", "utf-8"))
                    self.server_socket.send(bytes(f"{pseudo}:{mot_de_passe}", "utf-8"))
                    response = self.server_socket.recv(4096).decode('utf-8')

                    if response == "account_created":
                        print("Compte créé avec succès.")
                        break
                    else:
                        print("Erreur lors de la création du compte. Veuillez réessayer.")
                else:
                    print("Les mots de passe ne correspondent pas. Veuillez réessayer.")
            elif create_account_input == "non":
                print("Vous avez choisi de ne pas créer de compte. Déconnexion.")
                self.running = False
                break
            else:
                print("Réponse invalide. Veuillez répondre 'oui' ou 'non'.")

    def envoie_mesg(self):
        # Boucle pour envoyer des messages tant que le client est connecté au serveur
        while self.running:
            # Création du message souhaité
            destinataire = input("Entrez le pseudo du destinataire (ou 'tous' pour envoyer à tous): ")
            msg = input("Entrez votre message: ")
        
            # Envoi du message au serveur avec le pseudo du destinataire
            self.server_socket.send(bytes(f"{destinataire}:{msg}", 'utf-8'))

            # Si le message est '/exit
