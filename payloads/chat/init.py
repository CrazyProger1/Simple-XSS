"""Bad code of simple chat"""

from payload import event_handler, LocalWebsocketServer, Event, ClientSession, io

authorized = set()


@event_handler({'broadcast_message', })
async def on_broadcast_message(server: LocalWebsocketServer, session: ClientSession, event: Event):
    username = session.name
    message = event.data["message"]
    io.print(f'User {username} sent message {message}')
    await server.broadcast_event(authorized, event=Event(
        'message',
        data={
            'name': username,
            'message': message
        }
    ))


@event_handler({'set_name', })
async def on_set_name(server: LocalWebsocketServer, session: ClientSession, event: Event):
    session.name = event.data['name']
    io.print(f'User {session.name} connected')
    authorized.add(session)
