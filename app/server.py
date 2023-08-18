import asyncio
import json
from dataclasses import dataclass
from typing import Iterable

import textwrap
import websockets
from loguru import logger

from app.session import ClientSession
from app.utils import observer
from app.validators import validate_port, validate_host
from app.exceptions import MessageDecodeError, MessageEncodeError


@dataclass
class Event:
    """Attacker and client exchange events"""

    name: str
    data: dict


def decode_message(message: str) -> Event:
    """Decodes message to event"""

    try:
        data = json.loads(message)
        name = data.pop('event')
        return Event(name, data)
    except json.JSONDecodeError:
        raise MessageDecodeError('message is in wrong format')
    except Exception as e:
        raise MessageDecodeError(f'Error occurred during decoding message: {type(e).__name__}: {e}')


def encode_message(event: Event) -> str:
    """Encodes event to message"""

    try:
        data = {'event': event.name, **event.data}
        return json.dumps(data)
    except Exception as e:
        raise MessageEncodeError()


class LocalWebsocketServer:
    """
    Local server on the attacker PC.
    When a new connection is created, the server sends a payload to the client.
    After the payload is loaded, the client and the attacker can exchange events.
    """

    client_connected = observer.AsyncEvent()
    client_disconnected = observer.AsyncEvent()
    message_received = observer.AsyncEvent()
    event_received = observer.AsyncEvent()
    decode_error = observer.AsyncEvent()
    launched = observer.AsyncEvent()
    stopped = observer.AsyncEvent()

    @property
    def host(self) -> str:
        raise NotImplementedError

    @property
    def port(self) -> int:
        raise NotImplementedError

    @property
    def connected(self) -> set[ClientSession]:
        raise NotImplementedError

    async def send(self, session: ClientSession, message: str):
        raise NotImplementedError

    async def send_event(self, session: ClientSession, event: Event):
        raise NotImplementedError

    async def broadcast(self, sessions: Iterable[ClientSession], message: str):
        raise NotImplementedError

    async def broadcast_event(self, sessions: Iterable[ClientSession], event: Event):
        raise NotImplementedError

    async def broadcast_event_to_all(self, event: Event):
        raise NotImplementedError

    async def run(self):
        raise NotImplementedError

    async def stop(self):
        raise NotImplementedError


class DefaultWebsocketServer(LocalWebsocketServer):
    def __init__(self, host: str, port: int):
        validate_port(port)
        validate_host(host)
        self._host = host
        self._port = port
        self._connected = set()
        self._running = False

    async def _mainloop(self):
        while self._running:
            await asyncio.sleep(1)

    @staticmethod
    def _get_cons_from_sessions(sessions: Iterable[ClientSession]) -> list:
        connections = list([session.connection for session in sessions])
        return connections

    async def _handle_event(self, session: ClientSession, event: Event):
        await self.event_received(
            session=session,
            event=event
        )

    async def _handle_message(self, session: ClientSession, message: str):
        try:
            event = decode_message(message=message)
            logger.debug(f'Message decoded: {event.__dict__}')
        except MessageDecodeError as e:
            return await self.decode_error(error=e)

        await self._handle_event(
            session=session,
            event=event
        )

    async def _handle_connection(self, connection):
        session = ClientSession(
            connection=connection
        )
        self._connected.add(session)
        logger.debug(f'Client connected: {connection.origin}')
        await self.client_connected(session=session)

        try:
            async for message in connection:
                logger.debug(f'Message received: {message}')
                await self.message_received(
                    session=session,
                    message=message
                )
                await self._handle_message(
                    session=session,
                    message=message
                )
        except websockets.ConnectionClosedError:
            self._connected.remove(session)
            logger.debug(f'Client disconnected: {connection.origin}')
            await self.client_disconnected(session=session)

    @property
    def host(self):
        return self._host

    @property
    def port(self) -> int:
        return self._port

    @property
    def connected(self) -> set[ClientSession]:
        return self._connected

    async def send(self, session: ClientSession, message: str):
        logger.debug(f'Message sent: {textwrap.shorten(message, 100)}')
        await session.connection.send(str(message))

    async def send_event(self, session: ClientSession, event: Event):
        logger.debug(f'Event sent: {event.__dict__}')
        await session.connection.send(encode_message(event=event))

    async def broadcast(self, sessions: Iterable[ClientSession], message: str):
        logger.debug(f'Message broadcasted: {textwrap.shorten(message, 100)}')
        connections = self._get_cons_from_sessions(sessions)
        websockets.broadcast(connections, message)

    async def broadcast_event(self, sessions: Iterable[ClientSession], event: Event):
        logger.debug(f'Event broadcasted: {event.__dict__}')
        await self.broadcast(sessions, encode_message(event=event))

    async def broadcast_all(self, message: str):
        logger.debug(f'Message broadcasted to all: {textwrap.shorten(message, 100)}')
        connections = self._get_cons_from_sessions(self.connected)
        websockets.broadcast(connections)

    async def broadcast_event_to_all(self, event: Event):
        await self.broadcast_all(encode_message(event=event))

    async def stop(self):
        self._running = False

    async def run(self):
        self._running = True
        async with websockets.serve(self._handle_connection, self._host, self._port) as server:
            logger.info(f'Server is up: {self._host}:{self._port}')
            await self.launched(host=self._host, port=self._port)
            await self._mainloop()
            server.close(close_connections=True)
            logger.info(f'Server is down: {self._host}:{self._port}')
            await self.stopped(host=self._host, port=self._port)
