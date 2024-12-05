document.getElementById('send').addEventListener('click', sendMessage);
document.getElementById('message').addEventListener('keypress', function(e) {
    if (e.key === 'Enter' && !e.shiftKey) {
        e.preventDefault();
        sendMessage();
    }
});

function sendMessage() {
    var message = document.getElementById('message').value.trim();
    var image = document.getElementById('image').files[0];
    var formData = new FormData();

    if (message.length === 0 && !image) {
        return;
    }

    formData.append('message', message);
    if (image) {
        formData.append('image', image);
    }

    if (message.length > 0) { 
        addMessageToChat('user', message);
    }
    if (image) {
        addImageToChat('user', URL.createObjectURL(image));
    }

    fetch('/troubleshoot', {
        method: 'POST',
        body: formData
    })
    .then(response => response.json())
    .then(data => {
        if (data.response) {
            addMessageToChat('bot', data.response);
        } else if (data.error) {
            addMessageToChat('bot', `Error: ${data.error}`);
        }
    })
    .catch(error => {
        addMessageToChat('bot', `Error: ${error.message}`);
    });

    document.getElementById('message').value = '';
    document.getElementById('image').value = null;
}

function addMessageToChat(sender, text) {
    var chatBox = document.getElementById('chat-box');
    var messageDiv = document.createElement('div');
    messageDiv.className = sender === 'user' ? 'user-message' : 'bot-message';
    messageDiv.innerText = text;
    chatBox.appendChild(messageDiv);
    chatBox.scrollTop = chatBox.scrollHeight;
}

function addImageToChat(sender, imageUrl) {
    var chatBox = document.getElementById('chat-box');
    var imageDiv = document.createElement('div');
    imageDiv.className = sender === 'user' ? 'user-image' : 'bot-image';
    var img = document.createElement('img');
    img.src = imageUrl;
    imageDiv.appendChild(img);
    chatBox.appendChild(imageDiv);
    chatBox.scrollTop = chatBox.scrollHeight;
}
