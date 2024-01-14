from typing import Iterable

from .metaclasses import DeclarativeContainerMeta
from .types import BaseContainer, BaseDependency


class DeclarativeContainer(BaseContainer, metaclass=DeclarativeContainerMeta):
    @classmethod
    def configure(cls):
        pass

    @classmethod
    @property
    def dependencies(cls) -> Iterable["BaseDependency"]:
        dependencies = []

        for name, value in cls.__dict__.items():
            if isinstance(value, BaseDependency):
                dependencies.append(value)
        return dependencies
