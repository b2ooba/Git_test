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
            print("Connectée.")
        except Exception as e: # montre le message d'erreur pour la connexion au serveur (si il y en a)
            print("Erreur la connexion au serveur a echouée : ", str(e))

    def envoie_mesg(self):
        #Boucle pour envoyer des messages tant que le client et connectée  au serveur
        while self.running:
            #création du message souhaitée
            msg = input(f"{self.pseudo}> ")
            #Envoi du message au serveur
            self.server_socket.send(f"{self.pseudo} > {msg}".encode("utf-8"))
            # Si le message est exit, le client se déconnecte
            if msg == "/exit":
                print("Déconnection en cours.....")
                break
    
    
    def recevoir_msg (self):
        #Boucle pour recevoir des messages tant que le client est connectée au serveur
        while self.running:
            try:
                #Réception des données depuis le serveur
                data = self.server_socket.recv(1024).decode('utf-8')
                # Vérification si les donnéees ne sont pas vides
                if not data:
                    print("erreur")
                    self.running = False
                    break
                else: 
                    print(data)
            except Exception as e :
                print("erreur :", str(e))
                self.running = False
                break
    def start_threads (self):
        # Création des threads pour gérer l'envoi et la réception de messages simultanée
        envoyee_msg = threading.Thread(target=self.envoie_mesg)
        reception_msg = threading.Thread(target=self.recevoir_msg)
        # Démarrée les threads
        envoyee_msg.start()
        reception_msg.start()
client = Client()
client.start_threads()
