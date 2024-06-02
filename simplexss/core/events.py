from pyvents import EventChannel, AsyncEvent


class CoreEventChannel(EventChannel):
    application_launched = AsyncEvent()
    arguments_parsed = AsyncEvent()
    settings_loaded = AsyncEvent()
    plugins_loaded = AsyncEvent()
    application_terminated = AsyncEvent()
