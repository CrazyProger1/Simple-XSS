from src.utils import packages
from src.core.config import (
    HOOK_FILE,
    HOOK_CLASS_NAME
)


def load_hook(directory: str, loader: packages.PackageLoader = None):
    return loader.load(
        directory=directory,
        package_file=HOOK_FILE,
        package_class_name=HOOK_CLASS_NAME
    )


def load_hook_class(directory: str, loader: packages.PackageLoader = None):
    return loader.load_class(
        directory=directory,
        package_file=HOOK_FILE,
        package_class_name=HOOK_CLASS_NAME
    )
