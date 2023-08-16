import argparse
from app.utils import clss


class App(metaclass=clss.SingletonMeta):
    def __init__(self, namespace: argparse.Namespace):
        self._args = namespace

    @property
    def args(self) -> argparse.Namespace:
        return self._args

    async def run(self):
        raise NotImplementedError
