import inspect
from typing import Iterable, Callable
from app.session import ClientSession
from app.server import Event, encode_message, decode_message
from app.server import LocalWebsocketServer


def event_handler(events: Iterable[str]):
    event_set = set(events)

    def decorator(func):
        if not inspect.iscoroutinefunction(func):
            raise ValueError('Handler must be async')

        async def listener(server: LocalWebsocketServer, session: ClientSession, event: Event):
            if event.name in event_set:
                await func(server, session=session, event=event)

        LocalWebsocketServer.event_received.add_listener(listener, pass_subject=True)
        return func

    return decorator


__all__ = [
    'ClientSession',
    'Event',
    'LocalWebsocketServer',
    'encode_message',
    'decode_message',
    'event_handler'
]
