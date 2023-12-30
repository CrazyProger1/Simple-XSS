from typing import Callable

from loguru import logger
from typeguard import typechecked


class Event:
    _registered_events = set()

    @typechecked
    def __init__(self, name: str):
        logger.debug(f'Event {name} registered')
        self._listeners = {}
        self._last_instance = None
        self._name = name
        if self in self._registered_events:
            raise ValueError('Name must be unique')
        self._registered_events.add(self)

    @property
    def name(self):
        return self._name

    @classmethod
    @property
    def registered_events(cls) -> set:
        return cls._registered_events.copy()

    def _validate_listener(self, listener: Callable):
        if not callable(listener):
            raise ValueError('listener must be callable')

    def add_listener(self, listener: Callable, pass_subject: bool = False):
        self._validate_listener(listener=listener)
        if listener not in self._listeners.keys():
            self._listeners.update({listener: pass_subject})
            logger.debug(f'Added listener to {self._name} event')
        return listener

    def __eq__(self, other):
        return isinstance(other, Event) and self.name == other.name

    def __hash__(self):
        return hash(self.name)

    def __get__(self, instance, owner):
        self._last_instance = instance
        return self

    def __call__(self, **kwargs):
        logger.debug(f'Event {self._name} called')
        for listener, pass_subj in self._listeners.items():
            if pass_subj:
                listener(self._last_instance, **kwargs)
            else:
                listener(**kwargs)

    def __repr__(self):
        return f'<Event: {self._name}>'


class AsyncEvent(Event):
    _registered_events = set()

    async def __call__(self, **kwargs):
        logger.debug(f'Async Event {self._name} called')
        for listener, pass_subj in self._listeners.items():
            if pass_subj:
                await listener(self._last_instance, **kwargs)
            else:
                await listener(**kwargs)

    def __repr__(self):
        return f'<Async Event: {self._name}>'
