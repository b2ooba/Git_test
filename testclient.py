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

            # Recevoir la demande de mot de passe
            password_request_msg = self.server_socket.recv(1024).decode('utf-8')
            print(password_request_msg)

            # Envoyer le mot de passe au serveur
            password = input("Entrez votre mot de passe : ")
            self.server_socket.send(bytes(password, "utf-8"))

            print("Création de compte réussie.")
        except Exception as e:
            print("Erreur: la connexion au serveur a échoué -", str(e))
            self.running = False

    def send_message(self, message):
        self.server_socket.send(message.encode("utf-8"))

    def receive_messages(self):
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
