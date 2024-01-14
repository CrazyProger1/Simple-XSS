from src.utils import packages, di
from src.core.config import (
    HOOK_FILE,
    HOOK_CLASS_NAME
)

from .dependencies import HooksDependencyContainer


@di.inject
def load_hook(
        directory: str,
        loader: packages.PackageLoader = HooksDependencyContainer.hook_loader,
        base_class: type[packages.BasePackage] = HooksDependencyContainer.hook_base_class
):
    return loader.load(
        directory=directory,
        package_file=HOOK_FILE,
        package_class_name=HOOK_CLASS_NAME,
        base_class=base_class
    )


@di.inject
def load_hook_class(
        directory: str,
        loader: packages.PackageLoader = HooksDependencyContainer.hook_loader,
        base_class: type[packages.BasePackage] = HooksDependencyContainer.hook_base_class
):
    return loader.load_class(
        directory=directory,
        package_file=HOOK_FILE,
        package_class_name=HOOK_CLASS_NAME,
        base_class=base_class
    )


@di.inject
def is_hook(
        directory: str,
        loader: packages.PackageLoader = HooksDependencyContainer.hook_loader,
        base_class: type[packages.BasePackage] = HooksDependencyContainer.hook_base_class
) -> bool:
    return loader.is_package(
        directory=directory,
        package_file=HOOK_FILE,
        package_class_name=HOOK_CLASS_NAME,
        base_class=base_class
    )
