from src.utils import events

application_launched = events.Event('application_launched')
application_initialized = events.Event('application_initialized')
application_terminated = events.Event('application_terminated')
async_mode_entered = events.AsyncEvent('async_mode_entered')
