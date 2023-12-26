from abc import ABC, abstractmethod

from src.package import Package


class BaseHook(Package, ABC):
    TRANSPORT: str

    @property
    @abstractmethod
    def hook(self) -> str: ...
