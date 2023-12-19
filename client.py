import threading
import socket

class Client:
    def __init__(self, server_ip = "127.0.0.1", port=6666):
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.connect_to_server(server_ip, port)
        self.running = True
    
    def connect_to_server(self, ip, port):
        try:
            print("Connection en cours (°_°)")
            self.server_socket.connect((ip,port))
            print("Connectée.")
        except Exception as e:
            print("Erreur la connexion au serveur a echouée : ", str(e))

    def envoie_mesg(self):
        while True:
            msg = input()
            self.server_socket.send(msg.encode('utf-8'))
    def recevoir_msg (self):
        while True:
            try:
                data = self.server_socket.recv(4096).decode('utf-8')
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
        envoyee_msg = threading.Thread(target=self.envoie_mesg)
        reception_msg = threading.Thread(target=self.recevoir_msg)
        envoyee_msg.start()
        reception_msg.start()

client = Client()
client.start_threads()
