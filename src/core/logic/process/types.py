from abc import abstractmethod, ABC


class BaseProcess(ABC):

    @abstractmethod
    async def activate(self): ...

    @abstractmethod
    async def deactivate(self): ...
