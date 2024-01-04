from src.utils import events

ui_initialized = events.Event('ui_initialized')
ui_terminated = events.Event('ui_terminated')

ui_process_ran = events.AsyncEvent('ui_process_ran')
ui_process_stopped = events.AsyncEvent('ui_process_stopped')
