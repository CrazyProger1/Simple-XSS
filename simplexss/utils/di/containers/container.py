from typing import Collection

from ..types import (
    BaseContainer,
    BaseDependency
)


class Container(BaseContainer):
    @classmethod
    @property
    def dependencies(cls) -> Collection['BaseDependency']:
        return list(
            filter(
                lambda x: isinstance(x, BaseDependency),
                cls.__dict__.values()
            )
        )

    @classmethod
    def setup(cls):
        pass
