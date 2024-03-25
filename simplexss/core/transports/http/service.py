from .sessions import HTTPSession
from ..types import (
    BaseTransportService,
    BaseSession,
)


class HTTPService(BaseTransportService):
    NAME = 'Default HTTP Transport'
    PROTOCOL = 'http'

    def __init__(self):
        pass

    def run(self, host: str, port: int) -> BaseSession:
        session = HTTPSession(
            host=host,
            port=port,
            api=None,
        )

        return session

    def stop(self, session: BaseSession) -> None:
        pass
