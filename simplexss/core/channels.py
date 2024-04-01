from simplexss.utils.events import (
    EventChannel,
    AsyncEvent,
    Event
)


class CoreChannel(EventChannel):
    plugins_loaded = AsyncEvent()
    hooks_loaded = AsyncEvent()
    payloads_loaded = AsyncEvent()
    arguments_loaded = AsyncEvent()
    settings_loaded = AsyncEvent()
    core_initialized = Event()
    core_terminated = AsyncEvent()
