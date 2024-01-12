from src.utils import packages, di
from src.core.config import PLUGINS_DIRECTORY

from .managers import PluginManager
from .events import PluginsEventChannel
from .dependencies import PluginsDependencyContainer


@di.inject
def load_plugins(
        manager: PluginManager = PluginsDependencyContainer.plugin_manager,
        loader: packages.PackageLoader = PluginsDependencyContainer.plugin_loader
):
    plugins = manager.load_packages(PLUGINS_DIRECTORY, loader)
    PluginsEventChannel.plugins_loaded()
    return plugins
