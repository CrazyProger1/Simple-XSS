from abc import ABC, abstractmethod
from typing import Container

from src.utils import packages


class BasePayload(packages.BasePackage, ABC):
    TRANSPORT: Container[str]

    @abstractmethod
    def on_connection(self): ...

    @abstractmethod
    def on_event(self): ...
