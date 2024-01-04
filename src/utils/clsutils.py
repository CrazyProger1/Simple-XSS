import gc
from typing import Generator

from typeguard import typechecked


@typechecked
def iter_subclasses(cls: type, max_level: int = -1) -> Generator:
    if max_level == 0:
        return

    for subcls in cls.__subclasses__():
        yield subcls
        for subsubcls in iter_subclasses(subcls, max_level - 1):
            yield subsubcls


@typechecked
def iter_instances(cls: type) -> Generator:
    for instance in gc.get_objects():
        if isinstance(instance, cls):
            yield instance
