import pytest

from simplexss.utils.events import (
    EventChannel,
    Event,
    AsyncEvent
)


def test_event_channel_events_property():
    class Channel(EventChannel):
        event = Event()
        async_event = AsyncEvent()
        event_2 = Event()

    assert len(Channel.events) == 3
    assert Channel.event_2 in Channel.events
    assert Channel.async_event in Channel.events
    assert Channel.event in Channel.events
