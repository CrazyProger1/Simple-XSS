from src.utils import di
from src.utils import packages
from .managers import PluginManager


class PluginsDependencyContainer(di.DeclarativeContainer):
    plugin_manager: packages.BasePackageManager = PluginManager()
    plugin_loader: packages.BasePackageLoader = packages.PackageLoader()
