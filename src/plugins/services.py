from src.utils import di, packages
from .events import plugins_loaded
from .managers import PluginManager
from .dependencies import plugin_manager, plugin_loader
from .config import PLUGINS_DIRECTORY


@di.injector.inject
def load_plugins(
        manager: PluginManager = plugin_manager,
        loader: packages.PackageLoader = plugin_loader
):
    plugins = manager.load_packages(PLUGINS_DIRECTORY, loader)
    plugins_loaded()
    return plugins
