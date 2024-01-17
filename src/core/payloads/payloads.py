from typing import Container
from abc import abstractmethod

from src.core.enums import Protocol
from src.utils import packages, io


class BasePayload(packages.BasePackage):
    TRANSPORTS: Container[Protocol]

    io: io.AsyncIOManager

    async def on_launched(self, environment):
        pass

    async def on_stopped(self, environment):
        pass

    async def on_event(self, server, client, event):
        pass

    @property
    @abstractmethod
    def payload(self) -> str: ...
