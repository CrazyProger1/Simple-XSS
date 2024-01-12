import inspect

from .exceptions import DependencyNotBoundError
from .types import (
    BaseDependency,
    BaseContainer
)


class Dependency(BaseDependency):
    def __init__(self, name: str, base_type: type, container: BaseContainer, default: any):
        self._name = name
        self._base = base_type
        self._container = container
        self._default = default
        self._value = None

    def bind(self, value: any):
        if not isinstance(value, self._base) and not (inspect.isclass(value) and issubclass(value, self._base)):
            raise TypeError(f'Value must be instance or subclass of {self._base}, got {type(value)}')
        self._value = value

    @property
    def container(self) -> BaseContainer:
        return self._container

    @property
    def type(self) -> type:
        return self._base

    @property
    def value(self) -> type:
        value = self._value or self._default
        if not value:
            raise DependencyNotBoundError(self)
        return value

    @property
    def name(self) -> str:
        return self._name
