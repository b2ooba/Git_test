import threading
import socket

class Client:
    def __init__(self, server_ip="127.0.0.1", port=6666):
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.connect_to_server(server_ip, port)
        self.running = True
        self.pseudo = ""

    def connect_to_server(self, ip, port):
        try:
            print("Connexion en cours (°_°)")
            self.server_socket.connect((ip, port))
            print("Connecté.")

            # Création de compte
            create_account_msg = self.server_socket.recv(1024).decode('utf-8')
            print(create_account_msg)

            # Envoyer le pseudo au serveur
            pseudo = input("Entrez votre pseudo : ")
            self.server_socket.send(bytes(pseudo, "utf-8"))
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
                msg = self.server_socket.recv(1024).decode('utf-8')
                if not msg:
                    print("Erreur lors de la réception des messages.")
                    self.running = False
                    break
                else:
                    print(msg)
            except Exception as e:
                print("Erreur :", str(e))
                self.running = False
                break

    def start_threads(self):
        reception_thread = threading.Thread(target=self.receive_messages)
        reception_thread.start()

        while self.running:
            message = input(f"{self.pseudo}> ")
            if message.lower() == "/exit":
                print("Déconnexion en cours...")
                self.send_message("/exit")
                self.running = False
            else:
                self.send_message(message)

        reception_thread.join()

# Utilisation du client
client = Client()
client.start_threads()
#fd
#