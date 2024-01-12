from src.utils import events


class PluginsEventChannel(events.EventChannel):
    plugins_loaded = events.Event()
