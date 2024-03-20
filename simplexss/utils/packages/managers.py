import os
from typing import Iterable, Container

from .constants import (
    DEFAULT_PACKAGE_FILE,
    DEFAULT_PACKAGE_CLASS,
    DEFAULT_PACKAGES_DIR
)
from .types import (
    BasePackageManager,
    BasePackage
)
from .exceptions import (
    PackageNotLoadedError,
    PackageNotFoundError,
    PackageError,
    PackageDisabledError,
    PackageFormatError
)
from ..imputils import import_class


class PackageManager(BasePackageManager):
    def __init__(self, disabled: Container[str] = ()):
        self._packages = {}
        self._disabled = disabled

    def load_package(self, path: str, **kwargs) -> BasePackage:
        filename = kwargs.get('file', kwargs.get('filename', DEFAULT_PACKAGE_FILE))
        class_name = kwargs.get('class_name', DEFAULT_PACKAGE_CLASS)
        base_class = kwargs.get('base_class', BasePackage)

        if os.path.isdir(path):
            main_file = os.path.join(path, filename)
        else:
            main_file = path

        if not os.path.isfile(main_file):
            raise PackageNotFoundError(main_file)

        try:
            package_class = import_class(
                path=main_file,
                class_name=class_name,
                base=base_class
            )
        except (ImportError, TypeError):
            raise PackageFormatError(main_file)

        try:
            if package_class.NAME in self._disabled:
                raise PackageDisabledError(package_class.NAME)
        except AttributeError:
            raise PackageFormatError(main_file, 'Package {package} name not set')

        package = package_class()
        package.on_loaded(main_file)
        return package

    def load_packages(self, directory: str = DEFAULT_PACKAGES_DIR, **kwargs) -> Iterable[BasePackage]:
        for package in os.listdir(directory):
            package = os.path.join(directory, package)
            try:
                if os.path.isdir(package):
                    self.load_package(package, **kwargs)
            except PackageError as e:
                pass
        return self.packages

    def unload_package(self, name: str):
        package = self.get_package(name)

        if package is None:
            raise PackageNotLoadedError(name)

    def unload_packages(self):
        for name in self._packages.keys():
            self.unload_package(name)

    def get_package(self, name: str) -> BasePackage | None:
        return self._packages.get(name)

    @property
    def packages(self) -> Iterable[BasePackage]:
        return self._packages.values()
