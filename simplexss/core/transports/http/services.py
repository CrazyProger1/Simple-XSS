from .sessions import HTTPSession
from .types import (
    BaseHTTPTransportServer,
)
from .fastapi import (
    FastAPIServer,
)
from ..types import (
    BaseTransportService,
    BaseSession,
)
from ..exceptions import TransportError


class HTTPService(BaseTransportService):
    NAME = 'Default HTTP Transport'
    PROTOCOL = 'http'

    def __init__(self):
        self._sessions = {}

    async def run(
            self,
            host: str,
            port: int,
            server: BaseHTTPTransportServer = None,
            **kwargs
    ) -> BaseSession:
        if not server:
            server = FastAPIServer()

        api = await server.run(
            host=host,
            port=port,
        )

        session = HTTPSession(
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
