from src.utils import events

async_mode_entered = events.AsyncEvent('async_mode_entered')
application_initialized = events.Event('application_initialized')
application_launched = events.Event('application_launched')
application_terminated = events.Event('application_terminated')
