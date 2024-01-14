import inspect
from typing import Callable

from .dependencies import BaseDependency


def inject(clb: Callable):
    def inject_dependencies(kwargs):
        signature = inspect.signature(clb)
        for param_name, param in signature.parameters.items():
            if param_name not in kwargs:
                default = param.default
                if isinstance(default, BaseDependency):
                    kwargs.update({param_name: default.value})

    def wrapper(*args, **kwargs):
        inject_dependencies(kwargs)
        return clb(*args, **kwargs)

    async def async_wrapper(*args, **kwargs):
        inject_dependencies(kwargs)
        return await clb(*args, **kwargs)

    if inspect.iscoroutinefunction(clb):
        return async_wrapper
    return wrapper


def bind(dependency: any, value: any):
    dependency.bind_value(value)


def get(dependency: any) -> any:
    return dependency.value
