from src.utils import packages
from src.core.config import (
    PAYLOAD_FILE,
    PAYLOAD_CLASS_NAME
)


def load_payload(directory: str, loader: packages.PackageLoader = None):
    return loader.load(
        directory=directory,
        package_file=PAYLOAD_FILE,
        package_class_name=PAYLOAD_CLASS_NAME
    )


def load_payload_class(directory: str, loader: packages.PackageLoader = None):
    return loader.load_class(
        directory=directory,
        package_file=PAYLOAD_FILE,
        package_class_name=PAYLOAD_CLASS_NAME
    )
