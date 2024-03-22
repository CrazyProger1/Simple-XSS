from abc import (
    ABC,
    abstractmethod
)
from typing import Iterable


class BaseTransportService(ABC):
    name: str
    protocol: str

    


class BaseTransportServiceFactory(ABC):
    @abstractmethod
    def create(self, name: str): ...

    @abstractmethod
    def get_service(self, name: str) -> type[BaseTransportService] | None: ...

    @abstractmethod
    def get_names(self) -> Iterable[str]: ...
