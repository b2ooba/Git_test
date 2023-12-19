import tkinter as tk
from tkinter import PhotoImage

# Dictionnaire de couleur
couleur = {"nero": "#252726", "purple": "#800080", "white": "#FFFFFF"}

# Paramétrage fenêtre
app = tk.Tk()
app.title("My app")
app.config(bg="gray30")
app.geometry("400x600")
app.iconbitmap("logo.ico")

# Paramétrage Switch
btnEtat = False

# Chargement image Navbar
navIcon = PhotoImage(file='/Users/marjane/Git_test/marjane/menu.png')
closeIcon = PhotoImage(file='/Users/marjane/Git_test/marjane/close.png')
imgFond = PhotoImage(file='/Users/marjane/Git_test/marjane/back_image3.png')

# Définir les fonctions switch
def switch():
    global btnEtat
    if btnEtat:
        # Créer une fermeture animée Navbar
        for x in range(300):
            navLateral.place(x=-x, y=0)
            topFrame.update()
        btnEtat = False
    else:
        for x in range(-300, 0):
            navLateral.place(x=x, y=0)
            topFrame.update()
        btnEtat = True

# Top bar Navigation:
topFrame = tk.Frame(app, bg=couleur["purple"])
topFrame.pack(side="bottom", fill=tk.X)  # Modifié pour être en bas

# Texte de top bar
accueilText = tk.Label(topFrame, text="Java", font="ExtraCondensed 15",
                       bg=couleur["purple"], fg="white", height=2, padx=20)
accueilText.pack(side="right")

# Banner text & Image de fond
can = tk.Canvas(app, width=400, height=550)  # Hauteur ajustée
can.create_image(0, 0, anchor=tk.NW, image=imgFond)
bannerTexte = tk.Label(app, text="DEVELOPPEMENT", font="ExtraCondensed 25", fg="purple")
bannerTexte.place(x=50, y=350)  # Position ajustée
can.pack()

# Navbar Icone
navbarBtn = tk.Button(topFrame, image=navIcon, bg=couleur["purple"], bd=0, padx=20,
                      activebackground=couleur["purple"], command=switch)
navbarBtn.place(x=10, y=10)

# Paramètres Navbar Latérale
navLateral = tk.Frame(app, bg="gray30", width=300, height=600)
navLateral.place(x=-300, y=0)

# Les options dans la Navbar Laterale
option = ["ACCUEIL", "PAGES", "PROFIL", "PARAMETRES", "AIDE"]
y = 80
for i in range(5):
    tk.Button(navLateral, text=option[i], font="ExtraCondensed 15",
              bg="gray30", fg=couleur["white"], activebackground="gray30",
              bd=0).place(x=25, y=y)
    y += 40

# Paramétrage bouton fermeture menu
fermeBtn = tk.Button(navLateral, image=closeIcon, bg=couleur["purple"],
                     activebackground=couleur["purple"], bd=0, command=switch)
fermeBtn.place(x=250, y=10)

app.mainloop()
