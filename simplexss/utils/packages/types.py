from abc import ABC, abstractmethod
from typing import Iterable

from .constants import DEFAULT_PACKAGE_FILE, DEFAULT_PACKAGES_DIR


class BasePackage(ABC):
    NAME: str
    DESCRIPTION: str = None
    VERSION: str = "0.0.0"
    AUTHOR: str = None

    @abstractmethod
    def on_loaded(self, file: str): ...

    @abstractmethod
    def on_unloaded(self): ...


class BasePackageManager(ABC):
    @abstractmethod
    def load_package(self, path: str, **kwargs) -> BasePackage: ...

    @abstractmethod
    def load_packages(
        self, directory: str = DEFAULT_PACKAGES_DIR, **kwargs
    ) -> Iterable[BasePackage]: ...

    @abstractmethod
    def unload_package(self, name: str): ...

    @abstractmethod
    def unload_packages(self): ...

    @abstractmethod
    def get_package(self, name: str) -> BasePackage | None: ...

    @property
    @abstractmethod
    def packages(self) -> Iterable[BasePackage]: ...
