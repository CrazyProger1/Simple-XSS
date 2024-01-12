from .metaclasses import DeclarativeContainerMeta
from .types import BaseContainer


class DeclarativeContainer(BaseContainer, metaclass=DeclarativeContainerMeta):
    @classmethod
    def configure(cls):
        pass
