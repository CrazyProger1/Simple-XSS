from abc import ABC

from ..types import (
    BaseDependency,
    BaseContainer
)


class DependencyBasicFunctionality(BaseDependency, ABC):
    def __init__(self):
        self._container = None
        self._name = None

    def container(self) -> type[BaseContainer]:
        return self._container

    def __set_name__(self, owner: type[BaseContainer], name: str):
        if not issubclass(owner, BaseContainer):
            raise ValueError('Dependency can only be set to a container')

        self._container = owner
        self._name = name
