from app.utils import clss


class IOManager(metaclass=clss.SingletonMeta):
    """Allows you to work with input and output with any interface. See payloads for more info"""

    def print(self, *args) -> None:
        raise NotImplementedError

    def input(self, prompt: str) -> str | None:
        raise NotImplementedError
