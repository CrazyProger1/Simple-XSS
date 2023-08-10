from payload import event_handler, LocalWebsocketServer, Event, ClientSession


@event_handler({'hello', })
async def on_hello(server: LocalWebsocketServer, session: ClientSession, event: Event):
    await server.send(session, 'test')
    print('HELLO!')
