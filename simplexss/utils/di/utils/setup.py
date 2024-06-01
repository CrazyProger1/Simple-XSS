from ...clsutils import iter_subclasses
from ..types import BaseContainer


def setup(base: type[BaseContainer] = BaseContainer):
    for cls in iter_subclasses(base):
        cls: type[BaseContainer]
        cls.setup()
