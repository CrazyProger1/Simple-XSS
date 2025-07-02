from src.api import BasePlugin, CoreChannel, CoreContainer
from src.utils.di import inject


class Plugin(BasePlugin):
    NAME = "Settings Loading Detector"

    def on_loaded(self, file: str):
        CoreChannel.settings_loaded.subscribe(self.on_settings_loaded)

    @inject
    def on_settings_loaded(self, settings=CoreContainer.settings):
        print(f"Settings loaded: {settings}")
