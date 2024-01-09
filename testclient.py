"""mport threading
import socket

class Client:
    def __init__(self, server_ip="127.0.0.1", port=6666):
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.running = True
        self.connect_to_server(server_ip, port)

    def connect_to_server(self, ip, port):
        try:
            print("Connection en cours (°_°)")
            self.server_socket.connect((ip, port))
            pseudo = input("Entrez votre pseudo: ")
            self.pseudo = pseudo
            self.server_socket.send(bytes(pseudo, "utf-8"))
            self.handle_welcome_message()
        except Exception as e:
            print(f"Erreur la connexion au serveur a échoué : {str(e)}")

    def handle_welcome_message(self):
        message = self.server_socket.recv(4096).decode('utf-8')
        print(message)
        if "Veuillez créer un compte" in message:
            self.create_account()

    def create_account(self):
        pseudo = input("Entrer le pseudo que vous souhaitez utiliser: ")
        password = input("Entrer votre mot de passe: ")
        confirmation_password = input("Confirmez votre mot de passe: ")

        if password == confirmation_password:
            self.server_socket.send(bytes(f"CREATEACCOUNT {pseudo}:{password}", "utf-8"))
            response = self.server_socket.recv(4096).decode('utf-8').split("\n")[0]

            if response == "OK":
                print("Compte créé avec succès.")
                self.login()
            else:
                print("Erreur lors de la création du compte.")
        else:
            print("Les mots de passe ne correspondent pas.")

    def start_threads(self):
        reception_msg = threading.Thread(target=self.receive_msg)
        send_msg = threading.Thread(target=self.send_msg)
        reception_msg.start()
        send_msg.start()

    def send_msg(self):
        while self.running:
            msg = input(f"{self.pseudo}> ")
            self.msg = msg
            self.server_socket.send(f"{self.pseudo} > {msg}".encode("utf-8"))
            if msg == "/exit":
                print("Déconnection en cours.....")
                break

    def receive_msg(self):
        while True:
            try:
                self.msg = self.server_socket.recv(1024).decode('utf-8')
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

if __name__ == "__main__":
    client = Client()
    client.start_threads()
"""
import threading
import socket
from flask import Flask, render_template

app = Flask(__name__)

class Client:
    def __init__(self, server_ip="127.0.0.1", port=6666):
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.running = True
        self.connect_to_server(server_ip, port)

    def connect_to_server(self, ip, port):
        try:
            print("Connection en cours (°_°)")
            self.server_socket.connect((ip, port))
            pseudo = input("Entrez votre pseudo: ")
            self.pseudo = pseudo
            self.server_socket.send(bytes(pseudo, "utf-8"))
            self.handle_welcome_message()
        except Exception as e:
            print(f"Erreur la connexion au serveur a échoué : {str(e)}")

    def handle_welcome_message(self):
        message = self.server_socket.recv(4096).decode('utf-8')
        print(message)
        if "Veuillez créer un compte" in message:
            self.create_account()

    def create_account(self):
        pseudo = input("Entrer le pseudo que vous souhaitez utiliser: ")
        password = input("Entrer votre mot de passe: ")
        confirmation_password = input("Confirmez votre mot de passe: ")

        if password == confirmation_password:
            self.server_socket.send(bytes(f"CREATEACCOUNT {pseudo}:{password}", "utf-8"))
            response = self.server_socket.recv(4096).decode('utf-8').split("\n")[0]

            if response == "OK":
                print("Compte créé avec succès.")
                self.login()
            else:
                print("Erreur lors de la création du compte.")
        else:
            print("Les mots de passe ne correspondent pas.")

    def start_threads(self):
        reception_msg = threading.Thread(target=self.receive_msg)
        send_msg = threading.Thread(target=self.send_msg)
        reception_msg.start()
        send_msg.start()

    def send_msg(self):
        while self.running:
            msg = input(f"{self.pseudo}> ")
            self.msg = msg
            self.server_socket.send(f"{self.pseudo} > {msg}".encode("utf-8"))
            if msg == "/exit":
                print("Déconnection en cours.....")
                break

    def receive_msg(self):
        while True:
            try:
                self.msg = self.server_socket.recv(1024).decode('utf-8')
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

@app.route('/')
def index():
    return render_template('login_page.html')

@app.route('/signup')
def signup():
    return render_template('signup_page.html')

if __name__ == "__main__":
    client = Client()
    client.start_threads()
    app.run(debug=True)
