from src.utils import events

application_launched = events.Event('application_launched')
application_initialized = events.Event('application_initialized')
application_terminated = events.Event('application_terminated')

arguments_parsed = events.Event('arguments_parsed')

settings_loaded = events.Event('settings_loaded')

plugins_loaded = events.Event('plugins_loaded')

async_mode_entered = events.AsyncEvent('async_mode_entered')
