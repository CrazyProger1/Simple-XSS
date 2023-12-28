from abc import ABC, abstractmethod

from src.utils import packages


class BaseHook(packages.BasePackage, ABC):
    TRANSPORT: str

    @property
    @abstractmethod
    def hook(self) -> str: ...
