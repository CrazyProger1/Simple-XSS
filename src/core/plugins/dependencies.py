from src.utils import di
from src.utils import packages

plugin_manager = di.Dependency(packages.BasePackageManager)
plugin_loader = di.Dependency(packages.BasePackageLoader)
