from src.utils import events

settings_loaded = events.Event('settings_loaded')
settings_saved = events.Event('settings_saved')
