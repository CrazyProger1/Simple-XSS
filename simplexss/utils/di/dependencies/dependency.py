from .basic import DependencyBasicFunctionality


class Dependency(DependencyBasicFunctionality):
    def __init__(self, value: any):
        self._value = value
        super().__init__()

    @property
    def value(self) -> any:
        return self._value

    def __call__(self):
        return self.value
