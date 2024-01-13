from typing import Callable

from ...schemes import BaseClient, BaseEvent
from ...servers import BaseServer


class WebsocketServer(BaseServer):
    async def send(self, client: BaseClient, event: BaseEvent):
        pass

    def add_listener(self, callback: Callable[["BaseServer", BaseClient, BaseEvent], any]):
        pass

    async def run(self, host: str, port: int):
        pass

    async def stop(self):
        pass
