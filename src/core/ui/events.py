from src.utils import events

ui_initialized = events.Event('ui_initialized')
ui_terminated = events.Event('ui_terminated')


ui_process_activated = events.AsyncEvent('ui_process_activated')
ui_process_deactivated = events.AsyncEvent('ui_process_deactivated')
