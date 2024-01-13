import inspect
import os
from functools import cache

from .exceptions import DependencyNotBoundError
from .types import (
    BaseDependency,
    BaseContainer
)


class Dependency(BaseDependency):

    def __init__(
            self,
            default: any = None,
            allow_null: bool = False,
    ):
        self._name = None
        self._base = type(default)
        self._container = None
        self._default = default
        if default:
            self._check_value(default)
        self._value = None
        self._nullable = allow_null

    def _check_value(self, value: any):
        if not isinstance(value, self._base) and not (inspect.isclass(value) and issubclass(value, self._base)):
            raise TypeError(f'Value must be instance or subclass of {self._base}, got {type(value)}')

    def bind(self, name: str, base_type: type, default: any, container: BaseContainer):
        self._name = name
        self._base = base_type
        if default:
            self._check_value(default)
            self._default = default
        self._container = container

    def bind_value(self, value: any):
        self._check_value(value)
        self._value = value

    @property
    def container(self) -> BaseContainer:
        return self._container

    @property
    def type(self) -> type:
        return self._base

    @property
    def name(self) -> str:
        return self._name

    @property
    def value(self) -> any:
        value = self._value or self._default

        if not value and not self.nullable:
            raise DependencyNotBoundError(self)

        return value

    @property
    def nullable(self) -> bool:
        return self._nullable


class Factory(BaseDependency):
    def __init__(
            self,
            cls: type,
            *args,
            **kwargs
    ):
        self._class = cls
        self._args = args
        self._kwargs = kwargs

        self._name = None
        self._base = None
        self._container = None
        self._value = None

    def _check_value(self, value: any):
        if not (inspect.isclass(value) and issubclass(value, self._base)):
            raise TypeError(f'Value must be subclass of {self._base}, got {value}')

    def _inject_dependencies(self) -> tuple[list, dict]:
        args = []
        kwargs = {}

        for arg in self._args:
            if isinstance(arg, BaseDependency):
                args.append(arg.value)
            else:
                args.append(arg)

        for key, arg in self._kwargs.items():
            if isinstance(arg, BaseDependency):
                kwargs.update({key: arg.value})
            else:
                kwargs.update({key: arg})
        return args, kwargs

    def _create_instance(self, *args, **kwargs):
        return self._class(*args, **kwargs)

    def bind(self, name: str, base_type: type, default: any, container: BaseContainer):
        self._name = name
        self._base = base_type
        self._container = container

    def bind_value(self, value: any):
        self._check_value(value)
        self._class = value

    @property
    def container(self) -> BaseContainer:
        return self._container

    @property
    def type(self) -> type:
        return self._base

    @property
    def name(self) -> str:
        return self._name

    @property
    def value(self) -> any:
        args, kwargs = self._inject_dependencies()
        return self._create_instance(*args, **kwargs)

    @property
    def nullable(self) -> bool:
        return False


class Singleton(Factory):
    def __init__(self, cls: type, *args, **kwargs):
        super(Singleton, self).__init__(cls=cls, *args, **kwargs)

    @cache
    def _create_instance(self, *args, **kwargs):
        return super(Singleton, self)._create_instance(*args, **kwargs)

    @cache
    def _inject_dependencies(self) -> tuple[list, dict]:
        return super(Singleton, self)._inject_dependencies()

    def bind_value(self, value: any):
        self._create_instance.cache_clear()
        super(Singleton, self).bind_value(value=value)


class Environment(Dependency):
    def __init__(self, variable: str):
        super(Environment, self).__init__(
            default=os.getenv(variable),
            allow_null=False
        )
