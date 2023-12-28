import os
from abc import ABC, abstractmethod
from typing import Iterable

from loguru import logger

from .packages import BasePackage
from .loaders import BasePackageLoader, PackageLoader


class BasePackageManager(ABC):
    @abstractmethod
    def load_package(self, directory: str, loader: BasePackageLoader = None) -> BasePackage: ...

    @abstractmethod
    def load_packages(self, directory: str, loader: BasePackageLoader = None) -> Iterable[BasePackage]: ...


class PackageManager(BasePackageManager):
    def load_package(self, directory: str, loader: BasePackageLoader = None) -> BasePackage:
        if not loader:
            loader = PackageLoader()
        return loader.load(directory)

    def load_packages(self, directory: str, loader: BasePackageLoader = None) -> Iterable[BasePackage]:
        if not os.path.isdir(directory):
            logger.error(f'Directory {directory} not found')
            raise FileNotFoundError(f'Directory {directory} not found')

        result = []
        for package_directory in os.listdir(directory):
            package_directory = os.path.join(directory, package_directory)
            if os.path.isdir(package_directory):
                try:
                    package = self.load_package(
                        directory=package_directory,
                        loader=loader
                    )
                except ValueError:
                    continue
                result.append(package)
        logger.debug(f'Packages loaded from {directory}')
        return result
