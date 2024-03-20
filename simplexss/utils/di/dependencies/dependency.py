from contextlib import contextmanager

from .basic import DependencyBasicFunctionality


class Dependency(DependencyBasicFunctionality):
    def __init__(self, value: any = None):
        self._value = value
        super().__init__()

    def bind(self, value: any):
        self._value = value

    @contextmanager
    def temp_bind(self, value: any):
        old_value = self._value
        self.bind(value)

        yield

        self.bind(old_value)

    @property
    def value(self) -> any:
        return self._value

    def __call__(self):
        return self.value
