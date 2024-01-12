from src.utils import packages, di
from src.core.config import (
    PAYLOAD_FILE,
    PAYLOAD_CLASS_NAME
)
from .dependencies import PayloadsDependencyContainer


@di.inject
def load_payload(
        directory: str,
        loader: packages.PackageLoader = PayloadsDependencyContainer.payload_loader,
        base_class: type[packages.BasePackage] = PayloadsDependencyContainer.payload_base_class
):
    return loader.load(
        directory=directory,
        package_file=PAYLOAD_FILE,
        package_class_name=PAYLOAD_CLASS_NAME,
        base_class=base_class
    )


@di.inject
def load_payload_class(
        directory: str,
        loader: packages.PackageLoader = PayloadsDependencyContainer.payload_loader,
        base_class: type[packages.BasePackage] = PayloadsDependencyContainer.payload_base_class
):
    return loader.load_class(
        directory=directory,
        package_file=PAYLOAD_FILE,
        package_class_name=PAYLOAD_CLASS_NAME,
        base_class=base_class
    )


@di.inject
def is_payload(
        directory: str,
        loader: packages.PackageLoader = PayloadsDependencyContainer.payload_loader,
        base_class: type[packages.BasePackage] = PayloadsDependencyContainer.payload_base_class
):
    return loader.is_package(
        directory=directory,
        package_file=PAYLOAD_FILE,
        package_class_name=PAYLOAD_CLASS_NAME,
        base_class=base_class
    )
