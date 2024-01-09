from abc import ABC, abstractmethod

from .sessions import BaseSession


class BaseServer(ABC):
    def __init__(self, host: str, port: int):
        self._host = host
        self._port = port

    @abstractmethod
    async def stop(self): ...

    @abstractmethod
    async def run(self): ...

    @property
    @abstractmethod
    def session(self) -> BaseSession: ...

    @property
    def host(self) -> str:
        return self._host

    @property
    def port(self) -> int:
        return self._port

    def __repr__(self):
        return f'<Server: {self.host}:{self.port}>'
