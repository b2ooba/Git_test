# import socket
# import threading
# import sqlite3
# from flask import Flask, render_template, request

# # app = Flask(__name__)

# # # Initialisation du socket serveur TCP IPv4
# # server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# # IP, port = "127.0.0.1", 6666
# # server.bind((IP, port))
# # server.listen(10)
# # clients = []
# # pseudos = {}

# # # Diffusion des messages privés
# # def send_private_message(sender, receiver, message):
# #     if receiver in pseudos:
# #         receiver_client = pseudos[receiver]
# #         sender.send(bytes(f"Message privé pour {receiver}: {message}", "utf-8"))
# #         receiver_client.send(bytes(f"Message privé de {sender}: {message}", "utf-8"))
# #     else:
# #         sender.send(bytes(f"Erreur: {receiver} n'est pas connecté ou n'existe pas.", "utf-8"))

# # def broadcast(message, sender=None):
# #     for client in clients:
# #         if client != sender:
# #             client.send(bytes(message, "utf-8"))

# # def client_handler(client, pseudo):
# #     while True:
# #         try:
# #             message = client.recv(1024).decode("utf-8")
# #             if message == "/exit":
# #                 index = clients.index(client)
# #                 clients.remove(client)
# #                 pseudo = pseudos.pop(pseudo)
# #                 client.close()
# #                 broadcast(f"{pseudo} a quitté le chat!")
# #                 break
# #             elif message.startswith("@"):
# #                 # Format du message privé : @destinataire message
# #                 parts = message.split(" ", 1)
# #                 if len(parts) == 2:
# #                     send_private_message(pseudo, parts[0][1:], parts[1])
# #                 else:
# #                     client.send(bytes("Format incorrect pour le message privé. Utilisez @destinataire message", "utf-8"))
# #             else:
# #                 broadcast(f"{pseudo}: {message}", client)
# #         except:
# #             index = clients.index(client)
# #             clients.remove(client)
# #             pseudo = pseudos.pop(pseudo)
# #             client.close()
# #             broadcast(f"{pseudo} a quitté le chat!")
# #             break

# # # Connexion à la base de données SQLite
# # conn = sqlite3.connect('chat_database.db')
# # cursor = conn.cursor()

# # # Création de la table 'clients'
# # cursor.execute('''
# #     CREATE TABLE IF NOT EXISTS clients (
# #         id INTEGER PRIMARY KEY AUTOINCREMENT,
# #         pseudo TEXT UNIQUE,
# #         mdp TEXT
# #     )
# # ''')
# # conn.commit()

# # # Création de la table 'messages' pour stocker les messages
# # cursor.execute('''
# #     CREATE TABLE IF NOT EXISTS messages (
# #         id INTEGER PRIMARY KEY AUTOINCREMENT,
# #         expediteur TEXT,
# #         destinataire TEXT,
# #         message TEXT
# #     )
# # ''')
# # conn.commit()

# # # Fonction pour ajouter un client à la base de données
# # def add_client_to_db(pseudo, mdp, address, port):
# #     cursor.execute("INSERT INTO clients (pseudo, mdp) VALUES (?, ?)", (pseudo, mdp))
# #     conn.commit()

# # # Fonction pour vérifier les informations d'authentification d'un client
# # def verify_authentication(pseudo, mdp):
# #     cursor.execute("SELECT * FROM clients WHERE pseudo=? AND mdp=?", (pseudo, mdp))
# #     return cursor.fetchone() is not None

# # # Fonction pour stocker un message dans la base de données
# # def store_message_in_db(expediteur, destinataire, message):
# #     cursor.execute("INSERT INTO messages (expediteur, destinataire, message) VALUES (?, ?, ?)", (expediteur, destinataire, message))
# #     conn.commit()

# # # Fonction pour récupérer tous les messages entre deux utilisateurs
# # def retrieve_messages_from_db(expediteur, destinataire):
# #     cursor.execute("SELECT * FROM messages WHERE (expediteur=? AND destinataire=?) OR (expediteur=? AND destinataire=?) ORDER BY id", (expediteur, destinataire, destinataire, expediteur))
# #     return cursor.fetchall()

# # # Fonction pour gérer les connexions des clients
# # def handle_connections():
# #     local_conn = threading.local()
# #     local_conn.conn = sqlite3.connect('chat_database.db')
# #     local_conn.cursor = local_conn.conn.cursor()

# #     while True:
# #         client, adresse = server.accept()
# #         print(f"Connexion établie avec {str(adresse)}")

# #         # Page de création de compte
# #         client.send(bytes("Bienvenue ! Veuillez créer un compte ou vous connecter.\nEntrez votre pseudo : ", "utf-8"))
# #         pseudo = client.recv(1024).decode("utf-8").strip()

# #         # Vérifier si le client existe dans la base de données
# #         cursor.execute("SELECT * FROM clients WHERE pseudo=?", (pseudo,))
# #         existing_user = cursor.fetchone()

# #         if existing_user:
# #             # Client existe, demander le mot de passe pour authentification
# #             client.send(bytes("Entrez votre mot de passe : ", "utf-8"))
# #             mdp = client.recv(1024).decode("utf-8").strip()

# #             if verify_authentication(pseudo, mdp):
# #                 client.send(bytes(f"Bienvenue dans le chat, {pseudo}!\n", "utf-8"))
# #                 threading.Thread(target=client_handler, args=(client, pseudo)).start()
# #             else:
# #                 client.send(bytes("Erreur d'authentification. Fermeture de la connexion.", "utf-8"))
# #                 client.close()

# #         else:
# #             # Client n'existe pas, créer un nouveau compte
# #             client.send(bytes("Vous n'avez pas de compte. Entrez un mot de passe pour créer un compte : ", "utf-8"))
# #             mdp = client.recv(1024).decode("utf-8").strip()

# #             # Enregistrement des informations dans la base de données
# #             cursor.execute("INSERT INTO clients (pseudo, mdp) VALUES (?, ?)", (pseudo, mdp))
# #             conn.commit()

# #             # Informer le client que le compte a été créé avec succès
# #             client.send(bytes(f"Compte créé avec succès. Bienvenue, {pseudo}!\n", "utf-8"))
# #             threading.Thread(target=client_handler, args=(client, pseudo)).start()

# # if __name__ == "__main__":
# #     threading.Thread(target=handle_connections).start()
# #     threading.Thread(target=app.run).start()

# # app.py

# from flask import Flask, render_template, request, redirect, url_for
# from flask_sqlalchemy import SQLAlchemy
# from flask_socketio import SocketIO

# app = Flask(__name__)
# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///chat.db'
# db = SQLAlchemy(app)
# socketio = SocketIO(app)

# class User(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     username = db.Column(db.String(80), unique=True, nullable=False)
#     password = db.Column(db.String(120), nullable=False)

# class Message(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     content = db.Column(db.String(200), nullable=False)
#     user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
#     user = db.relationship('User', backref=db.backref('messages', lazy=True))

# # db.create_all()  # Ne pas créer les tables ici

# @app.route('/', methods=['GET', 'POST'])
# def login():
#     if request.method == 'POST':
#         # Si le formulaire est soumis, récupérez les données
#         username = request.form['username']
#         password = request.form['password']

#         # Ajoutez ici la logique d'authentification, par exemple, vérifiez si l'utilisateur existe dans la base de données

#         # Exemple simple de vérification, remplacez cela par votre propre logique
#         if username == 'utilisateur' and password == 'motdepasse':
#             flash('Login successful!', 'success')
#             return redirect(url_for('chat'))  # Redirigez vers la page de chat après la connexion
#         else:
#             flash('Invalid username or password. Please try again.', 'error')

#     # Si la méthode est GET ou si la connexion échoue, affichez simplement la page de connexion
#     return render_template('login.html')




# @socketio.on('message')
# def handle_message(msg):
#     print('Message:', msg)
#     socketio.emit('message', msg)

# @app.route('/signup', methods=['POST'])
# def register():
#     username = request.form['username']
#     password = request.form['password']
    
#     new_user = User(username=username, password=password)
#     db.session.add(new_user)
#     db.session.commit()



#     return redirect(url_for('index'))

# @app.route('/send_message', methods=['POST'])
# def send_message():
#     content = request.form['content']
#     user_id = 1  # Remplacez cela par la logique d'authentification de votre choix
    
#     new_message = Message(content=content, user_id=user_id)
#     db.session.add(new_message)
#     db.session.commit()

#     socketio.emit('message', f"{User.query.get(user_id).username}: {content}")

#     return redirect(url_for('login'))

# if __name__ == '__main__':
#     socketio.run(app, debug=True)



from flask import Flask, render_template, request, redirect, session, url_for
import threading
import json

app = Flask(__name__)
app.secret_key = "your_secret_key"  # Change this to a secure secret key

users = {}  # Dictionnaire pour stocker les utilisateurs et leurs mots de passe
messages = []  # Liste pour stocker les messages

def broadcast(message):
    for user, _ in users.items():
        if user != session["username"]:
            messages.append({"author": session["username"], "content": message})

@app.route('/')
def home():
    if 'username' in session:
        return redirect(url_for('chat'))
    return render_template('login.html')

@app.route('/login', methods=['POST'])
def login():
    username = request.form['username']
    password = request.form['password']
    if username in users and users[username] == password:
        session['username'] = username
        return redirect(url_for('chat'))
    else:
        return render_template('login.html', error='Invalid login credentials')

@app.route('/signup', methods=['POST'])
def signup():
    username = request.form['username']
    password = request.form['password']
    if username not in users:
        users[username] = password
        session['username'] = username
        return redirect(url_for('chat'))
    else:
        return render_template('signup.html', error='Username already exists')

@app.route('/chat')
def chat():
    if 'username' not in session:
        return redirect(url_for('home'))
    return render_template('interface1.html', username=session['username'], messages=messages)

@app.route('/send_message', methods=['POST'])
def send_message():
    message = request.form['message']
    broadcast(message)
    return redirect(url_for('chat'))

@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('home'))

if __name__ == '__main__':
    app.run(debug=True)
