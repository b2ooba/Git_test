# import tkinter as tk
# import socket
# import select 

# serveur = socket.socket (socket.AF_INET, socket.SOCK_STREAM)
# host, port = "127.0.0.1", 6666
# serveur.bind((host, port))
# serveur.listen(4)
# client_connectee = True
# socket_objs = [serveur]

# print("Bienvenu dans la conversation !!!")

# while client_connectee:
#     liste_Lu , liste_access_Ecrit, exception = select.select(socket_objs, [], socket_objs)
#     for socket_obj in liste_Lu:
        
#         #Nouvelle connexion entrante 
#         if socket_obj is serveur:
#             client, adresse = serveur.accept()
#             print(f"l'object client socket: {client} - adress: {adresse}")
#             socket_objs.append(client)
        
#         #Données réçus d'un client  
#         else:
#             donnee_reçus = socket_obj.recv(128).decode("utf-8")

#             if donnee_reçus:
#                 print(donnee_reçus)

#             #Le client s'est connectée
#             else:
#                 socket_objs.remove(socket_obj)
#                 print("Un participant est déconnecté")
#                 print(f"{len(socket_objs) - 1} participants restant")




"""Interface graphique"""
# from tkinter import *

# app = tk.Tk()
# app.title("Mon application")
# app.config(bg="gray30")
# app.geometry("400x600")

# app.mainloop()



import tkinter as tk  #T kinter pour la création de l'interface utilisateur.
from tkinter import messagebox  # classe messagebox du module Tkinter pour afficher des boîtes de dialogue
import socket   # gestioon de socket 
import select   # gestion Tkinter pour afficher des boîtes de dialogue


"""Classe ServerAPP"""
class ServerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Messagerie Serveur")

        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # Création d'un socket TCP IPv4 
        self.host, self.port = "127.0.0.1", 6666   # Adresse IP du serveur et le port d'écoute
        self.server_socket.bind((self.host, self.port))  # Associe le socket à l'adresse et au port spécifiés
        self.server_socket.listen(50)  # Met le serveur en mode écoute pour jusqu'à 50 connexions entrantes
        self.client_connected = False  # Indicateur de connexion client.
        self.socket_objs = [self.server_socket] # Liste des sockets à surveiller.




        self.create_gui() # Appelle la méthode create_gui pour créer l'interface utilisateur

    def create_gui(self):
        self.message_listbox = tk.Listbox(self.root, width=50, height=20)
        self.message_listbox.pack(pady=10)

        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)

        self.root.after(100, self.check_messages)
        self.root.mainloop()

    def on_closing(self):
        if messagebox.askokcancel("Quitter", "Voulez-vous vraiment quitter l'application?"):
            self.root.destroy()
            self.server_socket.close()

    def check_messages(self):
        try:
            readable, _, _ = select.select(self.socket_objs, [], [], 0)
            for socket_obj in readable:
                if socket_obj is self.server_socket:
                    client, address = self.server_socket.accept()
                    self.socket_objs.append(client)
                    self.client_connected = True
                    self.message_listbox.insert(tk.END, f"Connecté avec {address}")
                else:
                    data_received = socket_obj.recv(128).decode("utf-8")
                    if data_received:
                        self.message_listbox.insert(tk.END, f"Message reçu: {data_received}")
                    else:
                        self.socket_objs.remove(socket_obj)
                        self.message_listbox.insert(tk.END, "Un participant est déconnecté")
                        self.message_listbox.insert(tk.END, f"{len(self.socket_objs) - 1} participants restants")
                        if len(self.socket_objs) == 1:
                            self.client_connected = False
        except Exception as e:
            pass

        if self.client_connected:
            self.root.after(100, self.check_messages)


if __name__ == "__main__":
    root = tk.Tk()
    app = ServerApp(root)


