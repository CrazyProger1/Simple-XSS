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

    @property
    def value(self) -> any:
        if self._instance is None:
            self._instance = self._create_instance()

        return self._instance
