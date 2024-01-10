from src.utils import di

from src.api.plugins import BasePlugin
from src.api.events import ui_initialized
from src.api.dependencies import current_ui_dependency

from src.core.ui.base import BaseUI


class MyGUI(BaseUI):
    mode = 4

    def run(self):
        print('RUUUM')


class Plugin(BasePlugin):
    NAME = 'My Plugin'
    VERSION = '0.1'

    def __init__(self):
        ui_initialized.add_listener(self.on_ui_init)

    def on_ui_init(self):
        pass
        # di.injector.bind(current_ui_dependency, MyGUI())
