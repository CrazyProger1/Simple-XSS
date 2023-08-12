const connection = c;

function sendEvent(event, data) {
    connection.send(JSON.stringify({
        'event': event,
        ...data
    }))
}

fetch('https://api.ipify.org?format=json')
    .then(response => response.json())
    .then(data => sendEvent('print_ip', {'ip': data.ip}));
