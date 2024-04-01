from ..types import (
    BaseTransportService,
    BaseSession,
)
from ..exceptions import TransportError


class WebsocketService(BaseTransportService):
    NAME = 'Default Websocket Transport'
    PROTOCOL = 'websocket'

    def __init__(self):
        pass

    async def run(
            self,
            host: str,
            port: int,
            **kwargs
    ) -> BaseSession:
        print(host, port)

    async def stop(self, session: BaseSession) -> None:
        pass
