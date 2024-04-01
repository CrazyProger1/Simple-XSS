from typing import Collection

from .types import (
    BaseEvent,
    BaseEventChannel
)


class EventChannel(BaseEventChannel):
    @classmethod
    @property
    def events(cls) -> Collection[BaseEvent]:
        return list(
            filter(
                lambda x: isinstance(x, BaseEvent),
                cls.__dict__.values()
            )
        )
