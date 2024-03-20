from simplexss.api.plugins import Plugin as BasePlugin


class Plugin(BasePlugin):
    NAME = 'Simple-XSS plugin'

    def on_loaded(self, file: str):
        print(file)
