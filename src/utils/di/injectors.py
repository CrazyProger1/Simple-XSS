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
            raise ValueError(f'Value must be instance or subclass of {dependency.base}, got {value}')

    @typechecked
    def bind(self, dependency: Dependency, value: any):
        self._validate_value(dependency=dependency, value=value)

        logger.debug(f'Dependency {dependency} bound {value}')
        self._dependencies.update({dependency: value})

    @typechecked
    def inject(self, clb: Callable):

        def substitute_params(kwargs):
            signature = inspect.signature(clb)
            for param_name, param in signature.parameters.items():
                default = param.default
                if isinstance(default, Dependency):
                    if param_name not in kwargs:
                        kwargs.update({
                            param_name: self.get_dependency(default)
                        })

        def wrapper(*args, **kwargs):
            substitute_params(kwargs)
            return clb(*args, **kwargs)

        async def async_wrapper(*args, **kwargs):
            substitute_params(kwargs)
            return await clb(*args, **kwargs)

        if inspect.iscoroutinefunction(clb):
            return async_wrapper
        return wrapper

    @typechecked
    def get_dependency(self, dependency: Dependency, default: any = None):
        default = default or dependency.default

        value = self._dependencies.get(dependency, default)

        if value == default and callable(default):
            value = default()

        if not value:
            logger.error(f'Dependency not bound: {dependency}')
            raise ValueError(f'Dependency not bound: {dependency}')

        self._validate_value(dependency=dependency, value=value)
        return value


    @property
    def dependencies(self) -> dict:
        return self._dependencies.copy()
