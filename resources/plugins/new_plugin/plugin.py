from src.plugins import BasePlugin
from src.events import application_initialized
from src.core.launchers import GUILauncher
from src.core.dependencies import current_launcher
from src.utils import di


class MyLauncher(GUILauncher):
    def launch(self):
        print('LAUNCHED')
        super(MyLauncher, self)._launch()


class Plugin(BasePlugin):
    AUTHOR = 'crazyproger1'
    NAME = 'Test plugin'
    VERSION = '0.1'

    def __init__(self):
        application_initialized.add_listener(self.handle_application_initialized)

    def handle_application_initialized(self):
        di.injector.bind(current_launcher, MyLauncher())
