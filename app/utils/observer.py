import inspect
from typing import Callable


class Event:
    """Sync event"""

    def __init__(self, ):
        self._listeners = {}
        self._last_instance = None

    def __get__(self, instance, owner):
        self._last_instance = instance
        return self

    def add_listener(self, listener: Callable, pass_subject: bool = False):
        if not callable(listener):
            raise ValueError('listener must be callable')
        if listener not in self._listeners.keys():
            self._listeners.update({listener: pass_subject})

    def __call__(self, **kwargs):
        for listener, pass_subj in self._listeners.items():
            if pass_subj:
                listener(self._last_instance, **kwargs)
            else:
                listener(**kwargs)


class AsyncEvent(Event):
    """Async event"""

    def add_listener(self, listener: Callable, pass_subject: bool = False):
        if not inspect.iscoroutinefunction(listener) and inspect.ismethod(listener):
            raise ValueError('listener must be coroutine')

        super().add_listener(
            listener=listener,
            pass_subject=pass_subject
        )

    async def __call__(self, **kwargs):
        for listener, pass_subj in self._listeners.items():
            if pass_subj:
                await listener(self._last_instance, **kwargs)
            else:
                await listener(**kwargs)
