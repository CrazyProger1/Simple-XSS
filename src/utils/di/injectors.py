import inspect

from typing import Callable

from .dependencies import Dependency


class Injector:
    def __init__(self):
        self._dependencies = {}

    def bind(self, dependency: Dependency, value: any):
        base = dependency.base

        if not isinstance(value, base) and not \
                (inspect.isclass(dependency) and issubclass(value, base)):
            raise ValueError('Value must be instance or subclass of Dependency.base')

        self._dependencies.update({dependency: value})

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

    def get_dependency(self, dependency: Dependency):
        if dependency in self._dependencies:
            return self._dependencies[dependency]
        raise ValueError(f'Dependency not found: {dependency}')
