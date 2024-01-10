from src.utils import di
from src.utils import packages

plugin_manager_dependency = di.Dependency(packages.BasePackageManager)
plugin_loader_dependency = di.Dependency(packages.BasePackageLoader)
