TRANSPORT_JS_CODE = '''
const token = "{{ token }}";
const url = "{{ environment.url }}";
const listeners = {};

const sendEvent = async (event, data = {}) => {
    const options = {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'Authorization': token
        },
        body: JSON.stringify({
            'name': event,
            'data': data
        })
    };

    await fetch(url + '/event', options)
}


const addListener = (event, callback) => {
    if (!listeners[event]) {
        listeners[event] = [];
    }
    listeners[event].push(callback);
}

const listen = async () => {
    const options = {
        method: 'GET',
        headers: {
            'Content-Type': 'application/json',
            'Authorization': token
        },
    }
    while (true) {
        const response = await fetch(url + '/event', options)
        const data = await response.json();
        const callbacks = listeners[data.name]
        
        callbacks.forEach(callback => {
            callback(data.name, data.data);
        });
    }
}


listen()
'''
