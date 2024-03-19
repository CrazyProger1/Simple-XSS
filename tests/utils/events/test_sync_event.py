from simplexss.utils.events import (
    EventChannel,
    Event
)


def test_event_subscribe_publish():
    class Channel(EventChannel):
        event = Event()

    called = False

    def callback(event):
        nonlocal called

        assert event is Channel.event

        called = True

    Channel.event.subscribe(callback)
    Channel.event.publish()

    assert called
