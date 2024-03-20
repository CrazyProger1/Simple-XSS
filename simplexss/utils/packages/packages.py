from .types import BasePackage


class Package(BasePackage):

    def on_loaded(self, file: str):
        pass

    def on_unloaded(self):
        pass
