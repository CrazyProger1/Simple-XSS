from typing import Callable

from .factory import Factory


class Singleton(Factory):
    def __init__(self, factory: Callable, args: tuple = (), kwargs: dict = None):
        super().__init__(
            factory=factory,
            args=args,
            kwargs=kwargs
        )

        self._instance = None

    def _validate_instance(self, new):
        if self._instance is not None and not isinstance(new, type(self._instance)):
            raise TypeError(f'Instance must have a type of {type(self._instance)} not {type(new)}')

    def bind_instance(self, instance: any, strict: bool = True):
        if strict:
            self._validate_instance(instance)

        self._instance = instance

    @property
    def value(self) -> any:
        if self._instance is None:
            self._instance = self._create_instance()

        return self._instance
