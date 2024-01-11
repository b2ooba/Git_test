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
</script>