from src.utils import di
from src.utils import packages
from .managers import PluginManager

plugin_manager_dependency = di.Dependency(packages.BasePackageManager, default=PluginManager())
plugin_loader_dependency = di.Dependency(packages.BasePackageLoader, default=packages.PackageLoader())
