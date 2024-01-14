from abc import abstractmethod, ABC
from typing import Callable, Iterable

from loguru import logger
from typeguard import typechecked


class Event:

    @typechecked
    def __init__(self, name: str | None = None, required_kwargs: Iterable[str] | None = None):
        self._listeners = {}
        self._last_instance = None
        self._name = None
        self._required_kwargs = required_kwargs or ()
        self.name = name

    @staticmethod
    def _validate_listener(listener: Callable):
        if not callable(listener):
            raise ValueError('listener must be callable')

    def _check_kwargs(self, kwargs: dict):
        for key in self._required_kwargs:
            if not kwargs.get(key):
                raise TypeError(f"{self.name}() missing 1 required key argument: '{key}'")

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, value: str):
        if value:
            logger.debug(f'{self.__class__.__name__} {value} registered')
            self._name = value

    def add_listener(self, listener: Callable, pass_subject: bool = False):
        self._validate_listener(listener=listener)
        if listener not in self._listeners.keys():
            self._listeners.update({listener: pass_subject})
            logger.debug(f'Added listener to {self._name} event')
        return listener

    def __set_name__(self, owner, name):
        self.name = name

    def __eq__(self, other):
        return isinstance(other, Event) and self.name == other.name

    def __get__(self, instance, owner):
        self._last_instance = instance
        return self

    def __call__(self, **kwargs):
        self._check_kwargs(kwargs)
        logger.debug(f'Event {self._name} called')
        for listener, pass_subj in self._listeners.items():
            if pass_subj:
                listener(self._last_instance, **kwargs)
            else:
                listener(**kwargs)

    def __hash__(self):
        return hash(self.name)

    def __repr__(self):
        return f'<Event: {self._name}>'


class AsyncEvent(Event):
    async def __call__(self, **kwargs):
        self._check_kwargs(kwargs)
        logger.debug(f'Async Event {self._name} called')
        for listener, pass_subj in self._listeners.items():
            if pass_subj:
                await listener(self._last_instance, **kwargs)
            else:
                await listener(**kwargs)

    def __repr__(self):
        return f'<Async Event: {self._name}>'


class BaseEventChannel(ABC):
    @classmethod
    @property
    @abstractmethod
    def events(cls) -> Iterable[Event]: ...


class EventChannel(BaseEventChannel):

    @classmethod
    @property
    def events(cls) -> Iterable[Event]:
        events = set()

        for name, value in cls.__dict__.items():
            if isinstance(value, Event):
                events.add(value)
        return events
