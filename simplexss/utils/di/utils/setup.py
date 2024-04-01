from ..types import BaseContainer

from ...clsutils import (
    iter_subclasses,
)


def setup(base: type[BaseContainer] = BaseContainer):
    for cls in iter_subclasses(base):
        cls: type[BaseContainer]
        cls.setup()
