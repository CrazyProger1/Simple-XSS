from simplexss.api import (
    BasePlugin,
    CoreChannel,
)


class Plugin(BasePlugin):
    NAME = 'Settings Loading Detector'

    def on_loaded(self, file: str):
        CoreChannel.settings_loaded.subscribe(self.on_settings_loaded)

    def on_settings_loaded(self):
        print('SETTINGS LOADED!')
