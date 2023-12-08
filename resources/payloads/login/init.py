from payload import event_handler, io, LocalWebsocketServer, ClientSession, Event


@event_handler({'print', })
async def print_data(server: LocalWebsocketServer, session: ClientSession, event: Event):
    io.print(event.data.get('name', ''), event.data.get('content'))


@event_handler({'hello'})
async def connect(server: LocalWebsocketServer, session: ClientSession, event: Event):
    io.print(f'Client connected: {session.connection.origin}')
