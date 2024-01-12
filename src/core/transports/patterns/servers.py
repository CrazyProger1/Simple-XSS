from abc import ABC, abstractmethod

from .sessions import BaseSession


class BaseServer(ABC):

    @abstractmethod
    async def stop(self): ...

    @abstractmethod
    async def run(self): ...

    @property
    @abstractmethod
    def session(self) -> BaseSession: ...

    @property
    @abstractmethod
    def host(self) -> str: ...

    @property
    @abstractmethod
    def port(self) -> int: ...

    def __repr__(self):
        return f'<Server: {self.host}:{self.port}>'
