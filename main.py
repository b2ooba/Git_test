from flask import Flask, render_template, session, request, url_for, redirect
from flask_socketio import SocketIO, emit, join_room, leave_room, Namespace
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app)

# Structure pour stocker les informations basiques
users = {}  # Structure: {username: password_hash}
friends = {}  # Structure: {username: [list_of_friend_usernames]}
conversations = {}  # Structure: {(user1_username, user2_username): [messages]}

@app.route('/')
def index():
    # Supposons que l'utilisateur soit déjà authentifié pour cet exemple
    username = session.get('username')
    if not username:
        return redirect(url_for('login'))
    user_friends = friends.get(username, [])
    user_conversations = {friend: conversations.get((min(username, friend),max(username, friend)), []) for friend in user_friends}
    return render_template('index.html', conversations=user_conversations)


@app.route('/chat')
def chat():
    # Logique de la vue chat
    return render_template('chat.html')  # Assurez-vous d'avoir le bon chemin pour votre template


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        hashed_password = users.get(username)
        if hashed_password and check_password_hash(hashed_password, password):
            session['username'] = username  # Authentifier l'utilisateur
            return redirect(url_for('chat'))
        else:
            return "Nom d'utilisateur ou mot de passe incorrect!", 401
    return render_template('login.html')


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        if username not in users:
            users[username] = generate_password_hash(password)
            friends[username] = []  # Initialise liste d'amis vide
            return redirect(url_for('login'))
        else:
            return "Nom d'utilisateur déjà pris", 409
    return render_template('register.html')


# SocketIO events
@socketio.on('send_message')
def handle_send_message(json):
    sender = json['sender']
    receiver = json['receiver']
    message = json['message']

    # Ajout message dans 'conversations'
    convo_key = (min(sender, receiver), max(sender, receiver))
    if convo_key not in conversations:
        conversations[convo_key] = []
    conversations[convo_key].append({"sender": sender, "message": message})

    # Envoi en temps réel au destinataire si il est connecté
    emit('receive_message', json, room=receiver)


# Démarre l'application
if __name__ == '__main__':
    socketio.run(app, debug=True)
