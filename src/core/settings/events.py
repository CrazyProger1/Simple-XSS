from src.utils import events

class SettingsEventChannel(events.EventChannel):
    settings_loaded = events.Event()
    settings_saved = events.Event()
