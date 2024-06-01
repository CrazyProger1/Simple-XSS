import logging
import os
from typing import Container, Iterable

from ..imputils import import_class
from .constants import DEFAULT_PACKAGE_CLASS, DEFAULT_PACKAGE_FILE, DEFAULT_PACKAGES_DIR
from .exceptions import (
    PackageDisabledError,
    PackageError,
    PackageFormatError,
    PackageNotFoundError,
    PackageNotLoadedError,
)
from .types import BasePackage, BasePackageManager

logger = logging.getLogger("utils.packages")


class PackageManager(BasePackageManager):
    def __init__(self, disabled: Container[str] = ()):
        self._packages = {}
        self._disabled = disabled

    def load_package(self, path: str, **kwargs) -> BasePackage:
        filename = kwargs.get("file", kwargs.get("filename", DEFAULT_PACKAGE_FILE))
        class_name = kwargs.get("class_name", DEFAULT_PACKAGE_CLASS)
        base_class = kwargs.get("base_class", BasePackage)

        if os.path.isdir(path):
            main_file = os.path.join(path, filename)
        else:
            main_file = path

        if not os.path.isfile(main_file):
            raise PackageNotFoundError(main_file)

        try:
            package_class = import_class(
                path=main_file, class_name=class_name, base=base_class
            )
        except (ImportError, TypeError) as e:
            logger.error(e)
            raise PackageFormatError(main_file)

        try:
            if package_class.NAME in self._disabled:
                raise PackageDisabledError(package_class.NAME)
        except AttributeError as e:
            logger.error(e)
            raise PackageFormatError(main_file, "Package {package} name not set")

        try:
            package = package_class()
        except TypeError as e:
            logger.error(e)
            raise PackageFormatError(
                main_file, f"Package should implement all abstract methods"
            )

        package.on_loaded(main_file)
        self._packages[package.NAME] = package

        logger.debug(f"Package loaded: {package.NAME}")

        return package

    def load_packages(
        self, directory: str = DEFAULT_PACKAGES_DIR, **kwargs
    ) -> Iterable[BasePackage]:
        for package in os.listdir(directory):
            package = os.path.join(directory, package)
            try:
                if os.path.isdir(package):
                    self.load_package(package, **kwargs)
            except PackageError as e:
                logger.error(e)
        return self.packages

    def unload_package(self, name: str):
        package = self.get_package(name)

        if package is None:
            raise PackageNotLoadedError(name)

        logger.debug(f"Package unloaded: {name}")
        self._packages.pop(name)

    def unload_packages(self):
        for name in self._packages.keys():
            self.unload_package(name)

    def get_package(self, name: str) -> BasePackage | None:
        return self._packages.get(name)

    @property
    def packages(self) -> Iterable[BasePackage]:
        return self._packages.values()
