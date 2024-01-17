from abc import abstractmethod

from src.utils import packages, io
from src.core.enums import Protocol


class BaseHook(packages.BasePackage):
    TRANSPORT: Protocol
    io: io.AsyncIOManager

    async def on_launched(self, environment):
        pass

    async def on_stopped(self, environment):
        pass

    @property
    @abstractmethod
    def hook(self) -> str: ...
