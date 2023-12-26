import os
from abc import ABC, abstractmethod

from src.config import PLUGIN_FILE, PLUGIN_CLASS
from src.utils import imputils
from .plugins import BasePlugin


class BasePluginLoader(ABC):
    @classmethod
    @abstractmethod
    def load(cls, directory: str) -> BasePlugin: ...


class PluginLoader(BasePluginLoader):
    @classmethod
    def load(cls, directory: str) -> BasePlugin:
        plugin_file = os.path.join(directory, PLUGIN_FILE)
        if not os.path.isfile(plugin_file):
            raise ValueError(f'File {PLUGIN_FILE} not found at {directory}')

        plugin_class = imputils.import_class_by_filepath(
            plugin_file,
            PLUGIN_CLASS,
            base_class=BasePlugin
        )
        return plugin_class()
