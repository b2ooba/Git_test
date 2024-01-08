import threading
import socket
import asyncio
import websockets

class Client:
    def __init__(self, server_ip="127.0.0.1", port=6666):
        # Initialisation du socket serveur
        self.server_socket = None
        # Connection au serveur
        self.connect_to_server(server_ip, port)
        # État du client (actif ou non)
        self.running = True

    def connect_to_server(self, ip, port):
        try:
            print("Connection en cours (°_°)")
            # Connection au serveur WebSocket
            uri = f"ws://{ip}:{port}"
            self.server_socket = websockets.connect(uri)
            # Demande de pseudo au client
            pseudo = input("Entrez votre pseudo: ")
            self.pseudo = pseudo
            # Envoie du pseudo au serveur
            asyncio.get_event_loop().run_until_complete(self.server_socket)
            self.server_socket.send(pseudo)
            print("Connecté.")
        except Exception as e:
            print("Erreur la connexion au serveur a échoué : ", str(e))

    async def envoie_mesg(self):
        while self.running:
            msg = input(f"{self.pseudo}> ")
            self.msg = msg
            await self.server_socket.send(f"{self.pseudo} > {msg}")

            if msg == "/exit":
                print("Déconnexion en cours.....")
                break

    async def recevoir_msg(self):
        while True:
            try:
                msg = await self.server_socket.recv()
                if not msg:
                    print("erreur")
                    self.running = False
                    break
                else:
                    print(msg)
            except Exception as e:
                print("erreur :", str(e))
                self.running = False
                break

    def start_threads(self):
        loop = asyncio.get_event_loop()

        envoyee_msg = asyncio.ensure_future(self.envoie_mesg())
        reception_msg = asyncio.ensure_future(self.recevoir_msg())

        loop.run_until_complete(asyncio.gather(envoyee_msg, reception_msg))


client = Client()
client.start_threads()
