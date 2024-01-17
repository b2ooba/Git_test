document.addEventListener('DOMContentLoaded', function () {

    // Gestionnaire d'événements pour le bouton "Groupes"
    const groupButton = document.querySelector('#openPopupImage');
    groupButton.addEventListener('click', function () {
        
        fetch('/get_users')
            .then(response => response.json())
            .then(data => {
               
                console.log(data.users);
               
            })
            .catch(error => console.error('Erreur lors de la récupération des utilisateurs:', error));
    });

 });

// Gestionnaire d'événements pour le bouton "Groupes"
const groupButton = document.querySelector('#openPopupImage');
groupButton.addEventListener('click', function () {
    
    fetch('/get_users')
        .then(response => response.json())
        .then(data => {
            
            console.log(data.users);

            
            openPopup(data.users);
        })
        .catch(error => console.error('Erreur lors de la récupération des utilisateurs:', error));
});

// Fonction pour ouvrir le popup et afficher la liste des utilisateurs
function openPopup(userList) {
    const popup = document.getElementById('popup');
    const userListElement = document.getElementById('user-list');

   
    userListElement.innerHTML = '';

    
    userList.forEach(user => {
        const userElement = document.createElement('div');
        userElement.textContent = user;
        userListElement.appendChild(userElement);
    });

    
    popup.style.display = 'block';
}

// Fonction pour fermer le popup
function closePopup() {
    document.getElementById('popup').style.display = 'none';
}


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


// Fonction pour afficher la liste d'amis dans un pop-up
function viewFriends() {
    fetch('/view_friends')
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                const friendList = data.friend_usernames.join('\n');
                alert('Liste d\'amis:\n\n' + friendList);
            } else {
                alert('Erreur: ' + data.message);
            }
        })
        .catch(error => console.error('Erreur lors de la récupération de la liste d\'amis:', error));
}


var socket = io.connect('http://' + document.domain + ':' + location.port);
// Fonction pour envoyer un message
function sendMessage() {
    var messageInput = document.getElementById('message-input');
    var message = messageInput.value.trim();
    if (message !== "") {
        var receiver = "{{ receiver_username }}";  
        var json = {
            'sender': loggedInUsername,
            'receiver': receiver,
            'message': message
        };
      
        socket.emit('send_message', json);
        messageInput.value = "";
    }
}

// Événement SocketIO pour recevoir des messages
socket.on('receive_message', function(json) {
   
    displayMessage(json.sender, json.message);

   
    document.getElementById('message-input').value = "";
});



// Fonction pour afficher les messages reçus et envoyés
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

 
    chatBox.scrollTop = chatBox.scrollHeight;
}



