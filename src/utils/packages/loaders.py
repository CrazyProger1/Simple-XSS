import os
from abc import ABC, abstractmethod

from loguru import logger
from typeguard import typechecked

from .. import imputils
from .packages import BasePackage
from .config import PACKAGE_FILE, PACKAGE_CLASS_NAME


class BasePackageLoader(ABC):
    @classmethod
    @abstractmethod
    def is_package(
            cls,
            directory: str,
            package_file: str = PACKAGE_FILE,
            package_class_name: str = PACKAGE_CLASS_NAME) -> bool: ...

    @classmethod
    @abstractmethod
    def load_class(
            cls,
            directory: str,
            package_file: str = PACKAGE_FILE,
            package_class_name: str = PACKAGE_CLASS_NAME
    ) -> type[BasePackage]: ...

    @classmethod
    @abstractmethod
    def load(
            cls,
            directory: str,
            package_file: str = PACKAGE_FILE,
            package_class_name: str = PACKAGE_CLASS_NAME
    ) -> BasePackage: ...


class PackageLoader(BasePackageLoader):

    @classmethod
    @typechecked
    def is_package(
            cls,
            directory: str,
            package_file: str = PACKAGE_FILE,
            package_class_name: str = PACKAGE_CLASS_NAME) -> bool:
        try:
            cls.load_class(
                directory=directory,
                package_file=package_file,
                package_class_name=package_class_name
            )
            return True
        except (ValueError, TypeError, ImportError):
            return False

    @classmethod
    @typechecked
    def load_class(cls, directory: str, package_file: str = PACKAGE_FILE,
                   package_class_name: str = PACKAGE_CLASS_NAME) -> type[BasePackage]:
        package_file = os.path.join(directory, package_file)
        if not os.path.isfile(package_file):
            logger.error(f'File {package_file} not found at {directory}')
            raise ValueError(f'File {package_file} not found at {directory}')

        package_class = imputils.import_class_by_filepath(
            package_file,
            package_class_name,
            base_class=BasePackage
        )
        logger.debug(f'Package class loaded {package_class} from {directory}')
        return package_class

    @classmethod
    @typechecked
    def load(cls, directory: str,
             package_file: str = PACKAGE_FILE,
             package_class_name: str = PACKAGE_CLASS_NAME
             ) -> BasePackage:
        package_class = cls.load_class(
            directory=directory,
            package_file=package_file,
            package_class_name=package_class_name
        )
        package: BasePackage = package_class()
        logger.debug(f'Package loaded {package} from {directory}')
        package.bind(directory=directory)
        return package
