const connection = c;


connection.send(JSON.stringify({
    'event': 'hello',
    'asd': 'asdasd'
}))