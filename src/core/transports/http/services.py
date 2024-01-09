from src.core.enums import Protocol
from .servers import HTTPServer
from ..servers import BaseServer
from ..services import BaseTransportService
from ..sessions import BaseSession


class HTTPTransportService(BaseTransportService):
    name = 'http'
    protocol = Protocol.HTTP

    def __init__(self, server_class: type[BaseServer] = None):
        self._server_class = server_class or HTTPServer
        self._servers: dict[BaseSession, BaseServer] = {}

    async def run(self, host: str, port: int) -> BaseSession:
        server = self._server_class(host=host, port=port)
        session = server.session
        self._servers[session] = server
        await server.run()
        return session

    async def stop(self, session: BaseSession):
        server = self._servers.get(session)
        if server:
            await server.stop()
