import inspect
import logging
from functools import cache
from typing import Callable, Iterable

from .types import BaseAsyncEvent, BaseEvent, BaseEventChannel

logger = logging.getLogger("utils.events")


class Event(BaseEvent):
    def __init__(self, required_kwargs: Iterable[str] = ()):
        self._subscribers = []
        self._channel = None
        self._name = None
        self._required_kwargs = required_kwargs

    @staticmethod
    def _validate_callback(callback: Callable):
        if not callable(callback):
            raise ValueError("Callback must be a callable")

    @staticmethod
    @cache
    def _has_event_param(callback: Callable) -> bool:
        signature = inspect.signature(callback)
        params = signature.parameters
        return "event" in params

    def _check_kwargs(self, kwargs: dict):
        for arg in self._required_kwargs:
            if arg not in kwargs:
                raise ValueError(f"Argument is required: {arg}")

    def _inject_event(self, callback: Callable, kwargs: dict):
        if self._has_event_param(callback):
            kwargs.update({"event": self})

    def __set_name__(self, owner: type[BaseEventChannel], name: str):
        if not issubclass(owner, BaseEventChannel):
            raise ValueError("Event can only be set to an event channel")

        self._channel = owner
        self._name = name
        logger.info(f"Event registered: {name}")

    @property
    def channel(self) -> type[BaseEventChannel]:
        return self._channel

    def subscribe(self, callback: Callable):
        self._validate_callback(callback)
        if callback not in self._subscribers:
            self._subscribers.append(callback)
        logger.debug(f"Callback subscribed to {self._name}: {callback}")

    def publish(self, *args, **kwargs):
        self._check_kwargs(kwargs)
        for callback in self._subscribers:
            self._inject_event(callback, kwargs)
            callback(*args, **kwargs)
        logger.debug(f"Event published: {self._name}")


class AsyncEvent(BaseAsyncEvent, Event):
    async def publish_async(self, *args, **kwargs):
        self._check_kwargs(kwargs)
        for callback in self._subscribers:
            self._inject_event(callback, kwargs)
            if inspect.iscoroutinefunction(callback):
                await callback(*args, **kwargs)
            else:
                callback(*args, **kwargs)
        logger.debug(f"Event published async: {self._name}")
