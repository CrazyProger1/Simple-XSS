from src.utils import di
from .controllers import BaseController

current_controller = di.Dependency(BaseController)
