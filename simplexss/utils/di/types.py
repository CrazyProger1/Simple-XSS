from abc import (
    ABC,
    abstractmethod
)
from typing import Collection


class BaseContainer(ABC):
    @classmethod
    @property
    @abstractmethod
    def dependencies(cls) -> Collection['BaseDependency']: ...

    @classmethod
    @abstractmethod
    def setup(cls): ...


class BaseDependency(ABC):
    @property
    @abstractmethod
    def container(self) -> type[BaseContainer]: ...

    @property
    @abstractmethod
    def value(self) -> any: ...

    @abstractmethod
    def __call__(self): ...
