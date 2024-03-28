fetch('https://api.ipify.org?format=json')
    .then(response => response.json())
    .then(data => sendEvent('ip', {'ip': data.ip}));
