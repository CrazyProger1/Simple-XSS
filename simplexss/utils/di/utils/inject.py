import inspect
from functools import wraps
from typing import Callable

from ..types import BaseDependency


def inject_into_kwargs(**kwargs) -> dict:
    result = {}

    for key, dep in kwargs.items():
        result[key] = dep
        if isinstance(dep, BaseDependency):
            result[key] = dep.value
    return result


def inject_into_params(target: Callable) -> dict:
    signature = inspect.signature(target)
    params = signature.parameters
    default_values = {
        key: value.default
        for key, value in params.items()
        if value.default != inspect.Parameter.empty
    }
    return inject_into_kwargs(**default_values)


def async_inject(target: Callable):
    @wraps(target)
    async def wrapper(*args, **kwargs):
        injected = inject_into_params(target)
        injected.update(inject_into_kwargs(**kwargs))
        return await target(*args, **injected)

    return wraps(target)(wrapper)


def inject(target: Callable):
    if inspect.iscoroutinefunction(target):
        return async_inject(target)

    @wraps(target)
    def wrapper(*args, **kwargs):
        injected = inject_into_params(target)
        injected.update(inject_into_kwargs(**kwargs))
        return target(*args, **injected)

    return wrapper
