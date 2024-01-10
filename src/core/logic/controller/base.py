from abc import abstractmethod, ABC


class BaseController(ABC):
    @abstractmethod
    async def run(self): ...

