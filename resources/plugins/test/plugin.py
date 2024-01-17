from src.utils import di
from src.api.plugins import BasePlugin
from src.api.dependencies import GUIDependencyContainer
from src.api.events import GUIEventChannel


class Plugin(BasePlugin):
    NAME = 'My Test Plugin'
    VERSION = '0.1'
    DESCRIPTION = 'Plugin to change title'
    AUTHOR = 'crazyproger1'

    def __init__(self):
        GUIEventChannel.page_initialized.add_listener(self.change_title)

    @di.inject
    def change_title(self, page=GUIDependencyContainer.main_page):
        page.title = 'Test Title'
