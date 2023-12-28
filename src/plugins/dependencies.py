from src.utils import di, packages
from .managers import PluginManager

plugin_manager = di.Dependency(PluginManager)
plugin_loader = di.Dependency(packages.PackageLoader)