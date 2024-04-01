import asyncio
import queue
import websockets

from simplexss.core.transports import (
    BaseTransportAPI,
    CommonTransportAPI
)
from simplexss.utils.network import validate_port, validate_host
from simplexss.utils.theads import thread
from simplexss.core.transports.exceptions import (
    TransportError,
)
from ..types import BaseWebsocketServer


class WebsocketServer(BaseWebsocketServer):

    async def run(self, host: str, port: int) -> BaseTransportAPI:
        pass

    async def stop(self):
        pass
