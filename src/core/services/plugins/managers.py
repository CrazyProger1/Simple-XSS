from src.utils import packages
from src.core.config import (
    PLUGIN_FILE,
    PLUGIN_CLASS_NAME
)


class PluginManager(packages.PackageManager):
    def load_package(self, directory: str, loader=None):
        if not loader:
            loader = packages.PackageLoader()

        return loader.load(directory, PLUGIN_FILE, PLUGIN_CLASS_NAME)
