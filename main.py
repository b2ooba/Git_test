from flask import Flask, render_template, session, request, url_for, redirect
from flask_socketio import SocketIO, emit, join_room
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from flask import jsonify


app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///Base.sql'  # Remplacez 'site.db' par le nom de votre fichier de base de données
db = SQLAlchemy(app)
socketio = SocketIO(app)

# Modèles SQLAlchemy
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)

class Friend(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    friend_username = db.Column(db.String(20), nullable=False)

class Conversation(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user1_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    user2_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

class Message(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    conversation_id = db.Column(db.Integer, db.ForeignKey('conversation.id'), nullable=False)
    sender_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    message = db.Column(db.String(255), nullable=False)

# Routes
@app.route('/')
def index():
    # Supposons que l'utilisateur soit déjà authentifié pour cet exemple
    username = session.get('username')
    if not username:
        return redirect(url_for('login'))
    user_friends = Friend.query.filter_by(user_id=session.get('user_id')).all()
    user_conversations = {friend.friend_username: Conversation.query.filter(
        (Conversation.user1_id == session.get('user_id'), Conversation.user2_id == friend.user_id) |
        (Conversation.user1_id == friend.user_id, Conversation.user2_id == session.get('user_id'))
    ).all() for friend in user_friends}
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

        user = User.query.filter_by(username=username).first()
        if user and check_password_hash(user.password, password):
            session['user_id'] = user.id  # Authentifier l'utilisateur
            session['username'] = username
            return redirect(url_for('chat'))
        else:
            return "Nom d'utilisateur ou mot de passe incorrect!", 401
    return render_template('login.html')

"""Ajout fonction ajout d'amis """
@app.route('/add_friend', methods=['POST'])
def add_friend():
    if request.method == 'POST':
        username = session.get('username')
        friend_username = request.form['friend_username']

        # Vérifiez si l'utilisateur existe
        user = User.query.filter_by(username=username).first()
        friend = User.query.filter_by(username=friend_username).first()

        if not user or not friend:
            return jsonify({'success': False, 'message': 'Utilisateur introuvable'}), 400

        # Vérifiez si les utilisateurs ne sont pas déjà amis
        existing_friendship = Friend.query.filter_by(user_id=user.id, friend_username=friend_username).first()

        if existing_friendship:
            return jsonify({'success': False, 'message': 'Utilisateurs déjà amis'}), 400

        # Ajoutez les utilisateurs comme amis
        new_friendship = Friend(user_id=user.id, friend_username=friend_username)
        db.session.add(new_friendship)
        db.session.commit()

        return jsonify({'success': True, 'message': 'Ami ajouté avec succès'}), 200

# ...
"""FIN FONCTION"""

"""AJOUT FONCTION VOIR LISTE AMIS"""
# ...

@app.route('/view_friends')
def view_friends():
    username = session.get('username')

    if not username:
        return redirect(url_for('login'))

    user = User.query.filter_by(username=username).first()

    if not user:
        return redirect(url_for('login'))

    user_friends = Friend.query.filter_by(user_id=user.id).all()
    friend_usernames = [friend.friend_username for friend in user_friends]

    return render_template('view_friends.html', friend_usernames=friend_usernames)

"""FIN FONCTION LISTE AMIS"""


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        existing_user = User.query.filter_by(username=username).first()
        if not existing_user:
            new_user = User(username=username, password=generate_password_hash(password))
            db.session.add(new_user)
            db.session.commit()

            # Ajoute l'utilisateur à la session
            session['user_id'] = new_user.id
            session['username'] = username

            return redirect(url_for('login'))
        else:
            return "Nom d'utilisateur déjà pris", 409
    return render_template('register.html')


@app.route('/get_users', methods=['GET'])
def get_users():
    # Récupérez tous les utilisateurs de la base de données
    users = User.query.all()
    
    # Construisez une liste des noms d'utilisateur
    user_list = [user.username for user in users]

    # Retournez la liste des utilisateurs sous forme de réponse JSON
    return jsonify(users=user_list)


# SocketIO events
@socketio.on('send_message')
def handle_send_message(json):
    sender = json['sender']
    receiver = json['receiver']
    message = json['message']

    # Ajout message dans la base de données
    conversation = Conversation.query.filter(
        (Conversation.user1_id == session.get('user_id'), Conversation.user2_id == receiver) |
        (Conversation.user1_id == receiver, Conversation.user2_id == session.get('user_id'))
    ).first()
    if not conversation:
        conversation = Conversation(user1_id=session.get('user_id'), user2_id=receiver)
        db.session.add(conversation)
        db.session.commit()

    db.session.add(Message(conversation_id=conversation.id, sender_id=session.get('user_id'), message=message))
    db.session.commit()

    # Envoi en temps réel au destinataire s'il est connecté
    emit('receive_message', json, room=receiver)

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    socketio.run(app, debug=True)