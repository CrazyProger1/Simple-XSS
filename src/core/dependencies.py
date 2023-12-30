from src.utils import di
from src.core.launchers import BaseLauncher

current_launcher = di.Dependency(BaseLauncher)
