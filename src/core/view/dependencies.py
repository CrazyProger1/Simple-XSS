from src.utils import di
from .ui import BaseUI

current_ui = di.Dependency(BaseUI)
