from src.utils import packages
from src.core.config import PLUGINS_DIRECTORY
from .managers import PluginManager


def load_plugins(
        manager: PluginManager,
        loader: packages.PackageLoader = None
):
    plugins = manager.load_packages(PLUGINS_DIRECTORY, loader)
    return plugins
