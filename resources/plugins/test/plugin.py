from src.utils import di

from src.api.plugins import BasePlugin
from src.api.events import ui_initialized
from src.api.dependencies import current_ui

from src.core.ui.gui import GUI


class MyGUI(GUI):
    def run(self):
        print('RUN MY GUI!')
        super(MyGUI, self).run()


class Plugin(BasePlugin):
    NAME = 'My Plugin'
    VERSION = '0.1'

    def __init__(self):
        ui_initialized.add_listener(self.on_ui_init)

    def on_ui_init(self):
        di.injector.bind(current_ui, MyGUI())
