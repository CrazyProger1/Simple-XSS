from typeguard import typechecked

from src.core.enums import Protocol
from ..services import BaseTransportService
from ..sessions import BaseSession
from .servers import WebsocketServer


class WebsocketTransportService(BaseTransportService):
    name = 'websocket'
    protocol = Protocol.WEBSOCKET

    @typechecked
    def __init__(self, server: type[WebsocketServer] | None = None):
        self._server_class = server or WebsocketServer
        self._sessions_servers = {}

    @typechecked
    async def run(self, host: str, port: int) -> BaseSession:
        server = self._server_class(
            host=host,
            port=port
        )
        await server.run()
        session = server.session
        self._sessions_servers[session] = server
        return server.session

    @typechecked
    async def stop(self, session: BaseSession):
        server: WebsocketServer = self._sessions_servers.get(session)
        if server:
            await server.stop()
