from typing import Callable

from .basic import DependencyBasicFunctionality
from ..utils import inject_into_kwargs


class Factory(DependencyBasicFunctionality):
    def __init__(self, factory: Callable, args: tuple = (), kwargs: dict = None):
        if not callable(factory):
            raise ValueError('Factory must be callable')

        self._factory = factory
        self._args = args
        self._kwargs = kwargs or {}
        super().__init__()

    def _create_instance(self):
        return self._factory(
            *self._args,
            **inject_into_kwargs(**self._kwargs),
        )

    @property
    def value(self) -> any:
        return self._create_instance()

    def __call__(self):
        return self.value
