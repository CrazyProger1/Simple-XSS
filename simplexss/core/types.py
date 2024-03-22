from typing import Literal
from abc import (
    ABC,
    abstractmethod
)


class BaseCore(ABC):
    @abstractmethod
    async def run(self): ...
