from app.utils import clss


class IOManager(metaclass=clss.SingletonMeta):
    def print(self, *args) -> None:
        raise NotImplementedError

    def input(self, prompt: str) -> str | None:
        raise NotImplementedError
