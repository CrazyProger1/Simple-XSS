from simplexss.utils.events import (
    EventChannel,
    AsyncEvent,
    Event
)


class UIChannel(EventChannel):
    ui_initialized = Event()
    ui_terminated = AsyncEvent()

    process_launched = AsyncEvent()
    process_terminated = AsyncEvent()
