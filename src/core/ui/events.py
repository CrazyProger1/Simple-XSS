from src.utils import events

ui_initialized = events.Event('ui_initialized')
ui_terminated = events.Event('ui_terminated')

process_ran = events.Event('process_ran')
process_stopped = events.Event('process_stopped')
