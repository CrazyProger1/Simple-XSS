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
        const callback = listeners[data.name]
        callback(data.name, data.data)
    }
}

const addEventListener = (event, callback) => {
    listeners[event] = callback;
}

listen()
'''
