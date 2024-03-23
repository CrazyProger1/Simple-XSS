import inspect
from typing import Callable
from functools import cache

from .types import (
    BaseEventChannel,
    BaseEvent,
    BaseAsyncEvent
)
from .logging import logger


class Event(BaseEvent):
    def __init__(self):
        self._subscribers = []
        self._channel = None
        self._name = None

    @staticmethod
    def _validate_callback(callback: Callable):
        if not callable(callback):
            raise ValueError('Callback must be a callable')

    @staticmethod
    @cache
    def _has_event_param(callback: Callable) -> bool:
        signature = inspect.signature(callback)
        params = signature.parameters
        return 'event' in params

    def _inject_kwargs(self, callback: Callable, kwargs: dict):
        if self._has_event_param(callback):
            kwargs.update({'event': self})

    def __set_name__(self, owner: type[BaseEventChannel], name: str):
        if not issubclass(owner, BaseEventChannel):
            raise ValueError('Event can only be set to an event channel')

        self._channel = owner
        self._name = name
        logger.info(f'Event registered: {name}')

    @property
    def channel(self) -> type[BaseEventChannel]:
        return self._channel

    def subscribe(self, callback: Callable):
        self._validate_callback(callback)
        if callback not in self._subscribers:
            self._subscribers.append(callback)
        logger.debug(f'Callback subscribed to {self._name}: {callback}')

    def publish(self, *args, **kwargs):
        for callback in self._subscribers:
            self._inject_kwargs(callback, kwargs)
            callback(*args, **kwargs)
        logger.debug(f'Event published: {self._name}')


class AsyncEvent(BaseAsyncEvent, Event):
    async def publish_async(self, *args, **kwargs):
        for callback in self._subscribers:
            self._inject_kwargs(callback, kwargs)
            if inspect.iscoroutinefunction(callback):
                await callback(*args, **kwargs)
            else:
                callback(*args, **kwargs)
        logger.debug(f'Event published async: {self._name}')
