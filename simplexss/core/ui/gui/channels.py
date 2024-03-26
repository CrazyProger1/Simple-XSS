from simplexss.utils.events import (
    EventChannel,
    AsyncEvent,
    Event
)


class GUIChannel(EventChannel):
    need_update = AsyncEvent()
    process_launched = AsyncEvent()
    process_terminated = AsyncEvent()
