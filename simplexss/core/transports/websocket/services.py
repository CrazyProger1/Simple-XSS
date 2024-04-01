from .types import BaseWebsocketServer
from ..types import (
    BaseTransportService,
    BaseSession,
)
from ..exceptions import TransportError
from .server import WebsocketServer
from .sessions import WebsocketSession


class WebsocketService(BaseTransportService):
    NAME = 'Default Websocket Transport'
    PROTOCOL = 'websocket'

    def __init__(self):
        self._sessions = {}

    async def run(
            self,
            host: str,
            port: int,
            server: BaseWebsocketServer = None,
            **kwargs
    ) -> BaseSession:
        if server is None:
            server = WebsocketServer()

        api = await server.run(
            host=host,
            port=port,
        )

        session = WebsocketSession(
            host=host,
            port=port,
            api=api,
        )

        self._sessions[session] = server
        return session

    async def stop(self, session: BaseSession) -> None:
        server = self._sessions.get(session)
        if server is None:
            raise ValueError('Session not found')

        await server.stop()
