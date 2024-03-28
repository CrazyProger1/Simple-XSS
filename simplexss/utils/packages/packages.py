import os

from .types import BasePackage


class Package(BasePackage):
    file: str = None
    directory: str = None

    def on_loaded(self, file: str):
        self.file = file
        self.directory = os.path.dirname(file)

    def on_unloaded(self):
        pass
