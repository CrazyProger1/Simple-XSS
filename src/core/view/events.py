from src.utils import events


ui_initialized = events.AsyncEvent('interface_initialized')
ui_displayed = events.AsyncEvent('interface_displayed')
process_launched = events.AsyncEvent('process_launched')
process_terminated = events.AsyncEvent('process_terminated')
