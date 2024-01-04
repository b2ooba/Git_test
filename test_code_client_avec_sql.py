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
            print("Connecté.")
        except Exception as e:
            print("Erreur la connexion au serveur a échoué : ", str(e))

    def envoie_mesg(self):
        # Boucle pour envoyer des messages tant que le client est connecté au serveur
        while self.running:
            # Création du message souhaité
            destinataire = input("Entrez le pseudo du destinataire (ou 'tous' pour envoyer à tous): ")
            msg = input("Entrez votre message: ")
        
            # Envoi du message au serveur avec le pseudo du destinataire
            self.server_socket.send(bytes(f"{destinataire}:{msg}", 'utf-8'))

            # Si le message est '/exit', le client se déconnecte
            if msg == "/exit":
                print("Déconnexion en cours.....")
                break

    def recevoir_msg(self):
        # Boucle pour recevoir des messages tant que le client est connecté au serveur
        while True:
            try:
                # Réception des données depuis le serveur
                data = self.server_socket.recv(4096).decode('utf-8')
                # Vérification si les données ne sont pas vides
                if not data:
                    print("Erreur")
                    self.running = False
                    break
                else:
                    print(data)
            except Exception as e:
                print("Erreur :", str(e))
                self.running = False
                break

    def start_threads(self):
        # Création des threads pour gérer l'envoi et la réception de messages simultanée
        reception_msg = threading.Thread(target=self.recevoir_msg)
        envoyee_msg = threading.Thread(target=self.envoie_mesg)
        # Démarrée les threads
        reception_msg.start()
        envoyee_msg.start()

# Instanciation du client et démarrage des threads
client = Client()
client.start_threads()
