from src.utils import di

from src.api.plugins import BasePlugin
from src.api.events import UIEventChannel
from src.api.dependencies import UIDependencyContainer

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
        UIEventChannel.ui_initialized.add_listener(self.on_ui_init)

    def on_ui_init(self):
        di.bind(UIDependencyContainer.current_ui, MyGUI())
