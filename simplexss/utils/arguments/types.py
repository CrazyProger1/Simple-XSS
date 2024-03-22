import argparse
from abc import (
    ABC,
    abstractmethod
)
from typing import Sequence

from pydantic import BaseModel


class BaseSchemedArgumentParser(argparse.ArgumentParser, ABC):
    @abstractmethod
    def parse_schemed_args(
            self,
            args: Sequence[str] | None = None,
            namespace: argparse.Namespace | None = None
    ) -> BaseModel: ...
