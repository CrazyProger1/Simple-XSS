from simplexss.core.api import (
    BaseTransport,
)
from .server import FastAPIServer
from .types import BaseHTTPServer
from ..sessions import Session
from ..types import BaseTransportService


class HttpService(BaseTransportService):
    NAME = 'Default HTTP Transport'
    PROTOCOL = 'http'

    def __init__(self):
        self._running = {}

    async def run(
            self,
            host: str,
            port: int,
            api: BaseTransport,
            server: BaseHTTPServer = None,
            **kwargs
    ) -> Session:
        if server is None:
            server = FastAPIServer()

        await server.run(
            host=host,
            port=port,
            api=api
        )
        session = Session(
            host=host,
            port=port
        )
        self._running[session] = server
        return session

    async def stop(self, session: Session, **kwargs):
        server: BaseHTTPServer = self._running.get(session)
        if server is None:
            raise

        await server.stop()
        self._running.pop(session)
