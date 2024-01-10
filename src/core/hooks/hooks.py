from abc import abstractmethod

from src.utils import packages
from src.core.enums import Protocol


class BaseHook(packages.BasePackage):
    TRANSPORT: Protocol

    @property
    @abstractmethod
    def hook(self) -> str: ...
