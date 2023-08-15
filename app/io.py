from app.utils import clss


class IOManager(metaclass=clss.SingletonMeta):
    """Allows you to work with input and output with any interface. See payloads for more info"""

    debug: bool = True

    def print(self, *args) -> None:
        raise NotImplementedError

    def print_debug(self, *args):
        raise NotImplementedError

    def print_pos(self, *args):
        raise NotImplementedError

    def print_neg(self, *args):
        raise NotImplementedError

    def input(self, prompt: str) -> str | None:
        raise NotImplementedError
