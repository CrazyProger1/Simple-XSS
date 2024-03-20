from abc import (
    ABC,
    abstractmethod
)

from pydantic import BaseModel


class BaseLoader(ABC):
    @abstractmethod
    def load(self, file: str, schema: type[BaseModel], **kwargs) -> BaseModel: ...

    @abstractmethod
    def save(self, file: str, data: BaseModel, **kwargs): ...
