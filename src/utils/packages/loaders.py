import os
from abc import ABC, abstractmethod

from loguru import logger

from src.utils import imputils
from .packages import BasePackage
from .config import PACKAGE_FILE, PACKAGE_CLASS_NAME


class BasePackageLoader(ABC):
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
    def load(cls, directory: str,
             package_file: str = PACKAGE_FILE,
             package_class_name: str = PACKAGE_CLASS_NAME
             ) -> BasePackage:
        package_file = os.path.join(directory, package_file)
        if not os.path.isfile(package_file):
            logger.error(f'File {package_file} not found at {directory}')
            raise ValueError(f'File {package_file} not found at {directory}')

        package_class = imputils.import_class_by_filepath(
            package_file,
            package_class_name,
            base_class=BasePackage
        )
        logger.debug(f'Package loaded {package_class} from {directory}')
        package: BasePackage = package_class()
        package.bind(directory=directory)
        return package
