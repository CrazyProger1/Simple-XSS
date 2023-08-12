const connection = c;
const chatPage = `
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Chat Page</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            margin: 0;
            padding: 0;
            background-color: #f5f5f5;
        }

        .chat-container {
            max-width: 600px;
            margin: 50px auto;
            background-color: #fff;
            border-radius: 10px;
            box-shadow: 0 2px 5px rgba(0, 0, 0, 0.1);
            overflow: hidden;
        }

        .chat-header {
            padding: 15px;
            background-color: #007bff;
            color: #fff;
            text-align: center;
        }

        .chat-messages {
            padding: 15px;
            overflow-y: scroll;
            max-height: 400px;
        }

        .message {
            margin: 10px 0;
            padding: 10px;
            border-radius: 5px;
            background-color: #f0f0f0;
        }

        .message.sender {
            margin-left: auto;
            background-color: #007bff;
            color: #fff;
            text-align: right;
        }

        .message.receiver {
            margin-right: auto;
            background-color: #e5e5ea;
            text-align: left;
        }

        .message input[type="text"] {
            width: 95%;
            padding: 8px;
            border: 1px solid #ccc;
            border-radius: 5px;
        }

        .message button {
            margin-top: 5px;
            background-color: #007bff;
            color: #fff;
            border: none;
            border-radius: 5px;
            padding: 8px 15px;
            cursor: pointer;
        }
    </style>
</head>
<body>
<div class="chat-container">
    <div class="chat-header">
        <h2>{{metadata.name}} - V{{metadata.version}}</h2>
    </div>
    <div class="chat-messages" id="chat-messages">

    </div>
    <div class="message">
        <label>
            <input type="text" id="messageInput" placeholder="Type your message...">
        </label>
        <button id="sendMessageBtn">Send</button>
    </div>
</div>
</body>
</html>
`

function sendEvent(event, data) {
    connection.send(JSON.stringify({
        'event': event,
        ...data
    }))
}

function setName(name) {
    sendEvent('set_name', {
        'name': name
    })
}

function sendMessage(name, message) {
    sendEvent('broadcast_message', {
        'name': name,
        'message': message
    })
}


function addMessage(name, message, my = false) {
    const chatMessages = document.querySelector(".chat-messages");
    const msg_div = document.createElement("div");
    if (my) {
        msg_div.classList.add("message", "sender");
        msg_div.textContent = message;
    } else {
        msg_div.classList.add("message", "receiver");
        msg_div.textContent = "@" + name + ': ' + message;
    }


    chatMessages.appendChild(msg_div);
}

connection.onmessage = (e) => {
    let data = JSON.parse(e.data)

    switch (data.event) {
        case 'message':
            addMessage(data.name, data.message, data.name === name)
            break
    }
}

let name = null;

while (!name){
    name = prompt('Enter your name to start chatting:')
}
setName(name)
document.open()
document.write(chatPage)
document.close()
let sendMessageBtn = document.getElementById('sendMessageBtn')
sendMessage(name, 'connected to chat')

sendMessageBtn.addEventListener("click", function () {
    const messageInput = document.getElementById("messageInput");
    const messageText = messageInput.value;
    if (messageText !== '') {
        sendMessage(name, messageText)
    }
})