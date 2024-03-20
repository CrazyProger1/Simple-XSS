from .factory import Factory


class Singleton(Factory):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self._instance = None

    @property
    def value(self) -> any:
        if self._instance is None:
            self._instance = self._create_instance()

        return self._instance
