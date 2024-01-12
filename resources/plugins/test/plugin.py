from src.utils import di

from src.api.plugins import BasePlugin
from src.api.events import ui_initialized
from src.api.dependencies import current_ui_dependency

from src.core.ui.gui import GUI


class MyGUI(GUI):
    mode = 2

    async def run(self):
        print('RUUUM')
        await super(MyGUI, self).run()


class Plugin(BasePlugin):
    NAME = 'My Plugin'
    VERSION = '0.1'

    def __init__(self):
        ui_initialized.add_listener(self.on_ui_init)

    def on_ui_init(self):
        di.injector.bind(current_ui_dependency, MyGUI())
