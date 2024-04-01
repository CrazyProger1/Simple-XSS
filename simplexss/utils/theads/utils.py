import threading
from functools import wraps
from typing import Callable


def thread(target: Callable = None, /, *, daemon: bool = False):
    def wrapper(*args, **kwargs) -> threading.Thread:
        thr = threading.Thread(
            target=target,
            args=args,
            kwargs=kwargs,
            daemon=daemon
        )
        thr.start()
        return thr

    def decorator(func: Callable):
        nonlocal target

        target = func
        return wraps(target)(wrapper)

    if callable(target):
        return wraps(target)(wrapper)
    return decorator
