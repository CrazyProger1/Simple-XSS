from typing import Generator


def iter_subclasses(cls, max_level=-1) -> Generator:
    if max_level == 0:
        return

    for subcls in cls.__subclasses__():
        yield subcls
        for subsubcls in iter_subclasses(subcls, max_level - 1):
            yield subsubcls
