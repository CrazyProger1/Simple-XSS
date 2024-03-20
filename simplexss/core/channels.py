from simplexss.utils.events import (
    EventChannel,
    AsyncEvent
)


class CoreChannel(EventChannel):
    plugins_loaded = AsyncEvent()
    arguments_loaded = AsyncEvent()
    settings_loaded = AsyncEvent()
