from abc import ABC


class BasePackage(ABC):
    AUTHOR: str
    DESCRIPTION: str = None
    NAME: str
    VERSION: str

    def bind(self, directory: str):
        pass

    def __repr__(self):
        return f'<Package: {self.NAME} - V{self.VERSION}>'
