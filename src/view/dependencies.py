from src.utils import di
from .launchers import BaseLauncher

current_launcher = di.Dependency(BaseLauncher)
