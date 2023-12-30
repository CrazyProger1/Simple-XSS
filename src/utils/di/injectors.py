import inspect
from typing import Callable

from loguru import logger
from typeguard import typechecked

from .dependencies import Dependency


class Injector:
    def __init__(self):
        self._dependencies = {}

    def _validate_value(self, dependency: Dependency, value: any):
        base = dependency.base
        if not isinstance(value, base) and not \
                (inspect.isclass(value) and issubclass(value, base)):
            logger.error(f'Value must be instance or subclass of {dependency.base}, got {value}')
            raise ValueError('Value must be instance or subclass of Dependency.base')

    @typechecked
    def bind(self, dependency: Dependency, value: any):
        self._validate_value(dependency=dependency, value=value)

        logger.debug(f'Dependency {dependency} bound {value}')
        self._dependencies.update({dependency: value})

    @typechecked
    def inject(self, clb: Callable):
        def wrapper(*args, **kwargs):
            signature = inspect.signature(clb)
            for param_name, param in signature.parameters.items():
                default = param.default
                if isinstance(default, Dependency):
                    if param_name not in kwargs:
                        kwargs.update({
                            param_name: self.get_dependency(default)
                        })
            result = clb(*args, **kwargs)
            return result

        return wrapper

    @typechecked
    def get_dependency(self, dependency: Dependency, default: any = None):
        default = default or dependency.default

        value = self._dependencies.get(dependency, default)

        if value == default and callable(default):
            value = default()

        self._validate_value(dependency=dependency, value=value)

        if value:
            return value
        logger.error(f'Dependency not bound: {dependency}')
        raise ValueError(f'Dependency not bound: {dependency}')

    @property
    def dependencies(self) -> dict:
        return self._dependencies.copy()
