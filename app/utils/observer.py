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


class ResultEvent:
    def __init__(self, ):
        self._last_instance = None
        self._listener = None
        self._pass_subject = False

    def __get__(self, instance, owner):
        self._last_instance = instance
        return self

    def set_listener(self, listener: Callable, pass_subject: bool = False):
        if not callable(listener):
            raise ValueError('listener must be callable')

        self._listener = listener
        self._pass_subject = pass_subject

    def __call__(self, **kwargs):
        if self._listener:
            if self._pass_subject:
                self._listener(self._last_instance, **kwargs)
            else:
                self._listener(**kwargs)
