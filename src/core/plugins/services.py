from src.utils import packages, di
from src.core.config import PLUGINS_DIRECTORY

from .managers import PluginManager
from .events import plugins_loaded
from .dependencies import (
    plugin_manager_dependency,
    plugin_loader_dependency
)


@di.injector.inject
def load_plugins(
        manager: PluginManager = plugin_manager_dependency,
        loader: packages.PackageLoader = plugin_loader_dependency
):
    plugins = manager.load_packages(PLUGINS_DIRECTORY, loader)
    plugins_loaded()
    return plugins
