import tkinter as tk
import socket
import select 

serveur = socket.socket (socket.AF_INET, socket.SOCK_STREAM)
host = "127.0.0.1"
port = 6666
serveur.bind((host, port))
serveur.listen(4)
client_connectee = True
socket_objs = [serveur]

print("Bienvenu dans la conversation !!!")

while client_connectee:
    liste_Lu , liste_access_Ecrit, exception = select.select(socket_objs, [], socket_objs)
    for socket_obj in liste_Lu:
        
        #Nouvelle connexion entrante 
        if socket_obj is serveur:
            client, adresse = serveur.accept()
            socket_objs.append(socket_obj)
        
        #Données réçus d'un client 
        else:
            donnee_reçus = socket_obj.recv(128).decode("utf-8")

            if donnee_reçus:
                print(donnee_reçus)

            #Le client s'est connectée
            else:
                print("Un participant est déconnecté")
                print(f"{len(socket_objs) - 1} participants restant")     




"""Interface graphique"""
# from tkinter import *

# app = tk.Tk()
# app.title("Mon application")
# app.config(bg="gray30")
# app.geometry("400x600")

# app.mainloop()


