var socket = io.connect('http://' + document.domain + ':' + location.port);

// Function to send a message
function sendMessage() {
    var messageInput = document.getElementById('message-input');
    var message = messageInput.value.trim();

    if (message !== "") {
        // Utiliser la variable de session 'username' pour définir le destinataire
        var receiver = "{{ receiver_username }}";  // Mettez ici la logique pour choisir le destinataire

        var json = {
            'sender': "{{ session['username'] }}",
            'receiver': receiver,
            'message': message
        };

        socket.emit('send_message', json);
        messageInput.value = "";
    }
}

// chat.js

document.addEventListener('DOMContentLoaded', function () {
    // ... Autres initialisations ...

    // Gestionnaire d'événements pour le bouton "Groupes"
    const groupButton = document.querySelector('#openPopupImage');
    groupButton.addEventListener('click', function () {
        // Envoyez une requête au serveur pour obtenir la liste des utilisateurs
        fetch('/get_users')
            .then(response => response.json())
            .then(data => {
                // Manipulez la réponse du serveur (liste des utilisateurs)
                console.log(data.users);
                // Vous pouvez maintenant utiliser la liste des utilisateurs pour afficher ou effectuer d'autres actions
            })
            .catch(error => console.error('Erreur lors de la récupération des utilisateurs:', error));
    });

    // ... Autres gestionnaires d'événements ...
});

// Gestionnaire d'événements pour le bouton "Groupes"
const groupButton = document.querySelector('#openPopupImage');
groupButton.addEventListener('click', function () {
    // Envoyez une requête au serveur pour obtenir la liste des utilisateurs
    fetch('/get_users')
        .then(response => response.json())
        .then(data => {
            // Manipulez la réponse du serveur (liste des utilisateurs)
            console.log(data.users);

            // Affichez la liste des utilisateurs dans le popup
            openPopup(data.users);
        })
        .catch(error => console.error('Erreur lors de la récupération des utilisateurs:', error));
});

// Fonction pour ouvrir le popup et afficher la liste des utilisateurs
function openPopup(userList) {
    const popup = document.getElementById('popup');
    const userListElement = document.getElementById('user-list');

    // Effacez le contenu existant du popup
    userListElement.innerHTML = '';

    // Ajoutez chaque utilisateur à la liste du popup
    userList.forEach(user => {
        const userElement = document.createElement('div');
        userElement.textContent = user;
        userListElement.appendChild(userElement);
    });

    // Affichez le popup
    popup.style.display = 'block';
}

// Fonction pour fermer le popup
function closePopup() {
    document.getElementById('popup').style.display = 'none';
}

// AJOUT FONCTION AJOUT D'AMIS
// Fonction pour envoyer une demande d'ajout d'amis
function addFriend() {
    var friendInput = prompt("Entrez le nom d'utilisateur de votre ami:");

    if (friendInput) {
        fetch('/add_friend', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/x-www-form-urlencoded',
            },
            body: 'friend_username=' + friendInput,
        })
        .then(response => response.json())
        .then(data => {
            alert(data.message);
        })
        .catch(error => console.error('Erreur lors de l\'ajout d\'ami:', error));
    }
}

//FIN FONCTION AJOUT d'AMI


// Function to display received messages
function displayMessage(sender, content) {
    var chatBox = document.getElementById('chat-box');
    var messageDiv = document.createElement('div');
    messageDiv.classList.add('message');

    var senderSpan = document.createElement('span');
    senderSpan.classList.add('sender');
    senderSpan.textContent = sender + ': ';

    var contentSpan = document.createElement('span');
    contentSpan.classList.add('content');
    contentSpan.textContent = content;

    messageDiv.appendChild(senderSpan);
    messageDiv.appendChild(contentSpan);
    chatBox.appendChild(messageDiv);

    // Scroll to the bottom of the chat box
    chatBox.scrollTop = chatBox.scrollHeight;
}

// SocketIO event for receiving messages
socket.on('receive_message', function(json) {
    displayMessage(json.sender, json.message);
});