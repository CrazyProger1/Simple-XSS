import gc
from typing import Generator


def iter_subclasses(cls: type, max_level: int = -1) -> Generator:
    if max_level == 0:
        return

    for subcls in cls.__subclasses__():
        yield subcls
        for subsubcls in iter_subclasses(subcls, max_level - 1):
            yield subsubcls


def iter_instances(cls: type, precise: bool = True) -> Generator:
    for instance in gc.get_objects():
        if isinstance(instance, cls):
            instance_cls = instance.__class__
            if not precise:
                yield instance
            elif instance_cls == cls:
                yield instance
