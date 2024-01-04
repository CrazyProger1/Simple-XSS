from src.utils import packages, di
from src.core.config import PLUGINS_DIRECTORY
from src.core.dependencies import plugin_manager, plugin_loader
from .managers import PluginManager


@di.injector.inject
def load_plugins(
        manager: PluginManager = plugin_manager,
        loader: packages.PackageLoader = plugin_loader
):
    plugins = manager.load_packages(PLUGINS_DIRECTORY, loader)
    return plugins
