from src.utils import events

plugins_loaded = events.Event('plugins_loaded')
arguments_parsed = events.Event('arguments_parsed')
settings_loaded = events.Event('settings_loaded')
application_initialized = events.Event('application_initialized')
application_launched = events.AsyncEvent('application_launched')
application_terminated = events.Event('application_terminated')
