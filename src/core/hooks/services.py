from src.utils import packages, di
from src.core.config import (
    HOOK_FILE,
    HOOK_CLASS_NAME
)

from .dependencies import hook_loader_dependency


@di.injector.inject
def load_hook(directory: str, loader: packages.PackageLoader = hook_loader_dependency):
    return loader.load(
        directory=directory,
        package_file=HOOK_FILE,
        package_class_name=HOOK_CLASS_NAME
    )


@di.injector.inject
def load_hook_class(directory: str, loader: packages.PackageLoader = hook_loader_dependency):
    return loader.load_class(
        directory=directory,
        package_file=HOOK_FILE,
        package_class_name=HOOK_CLASS_NAME
    )


@di.injector.inject
def is_hook(directory: str, loader: packages.PackageLoader = hook_loader_dependency) -> bool:
    return loader.is_package(
        directory=directory,
        package_file=HOOK_FILE,
        package_class_name=HOOK_CLASS_NAME
    )
