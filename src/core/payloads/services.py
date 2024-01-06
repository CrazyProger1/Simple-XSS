from src.utils import packages, di
from src.core.config import (
    PAYLOAD_FILE,
    PAYLOAD_CLASS_NAME
)
from .dependencies import payload_loader


@di.injector.inject
def load_payload(directory: str, loader: packages.PackageLoader = payload_loader):
    return loader.load(
        directory=directory,
        package_file=PAYLOAD_FILE,
        package_class_name=PAYLOAD_CLASS_NAME
    )


@di.injector.inject
def load_payload_class(directory: str, loader: packages.PackageLoader = payload_loader):
    return loader.load_class(
        directory=directory,
        package_file=PAYLOAD_FILE,
        package_class_name=PAYLOAD_CLASS_NAME
    )


@di.injector.inject
def is_payload(directory: str, loader: packages.PackageLoader = payload_loader):
    return loader.is_package(
        directory=directory,
        package_file=PAYLOAD_FILE,
        package_class_name=PAYLOAD_CLASS_NAME
    )
