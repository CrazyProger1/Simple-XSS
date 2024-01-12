from src.utils import di, packages
from .hooks import BaseHook


class HooksDependencyContainer(di.DeclarativeContainer):
    hook_base_class: packages.BasePackage = BaseHook
    hook_loader: packages.BasePackageLoader = packages.PackageLoader()
