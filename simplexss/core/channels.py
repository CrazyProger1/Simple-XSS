from simplexss.utils.events import (
    EventChannel,
    AsyncEvent,
    Event
)


class CoreChannel(EventChannel):
    plugins_loaded = Event()
    hooks_loaded = Event()
    payloads_loaded = Event()
    arguments_loaded = Event()
    settings_loaded = Event()
    core_initialized = Event()
    core_terminated = AsyncEvent()
