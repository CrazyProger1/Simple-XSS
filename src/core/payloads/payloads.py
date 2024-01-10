from typing import Container
from abc import abstractmethod

from src.core.enums import Protocol
from src.utils import packages


class BasePayload(packages.BasePackage):
    TRANSPORTS: Container[Protocol]

    @property
    @abstractmethod
    def payload(self) -> str: ...
