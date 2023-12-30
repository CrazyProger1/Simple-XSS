from src.utils import events

controller_initialized = events.AsyncEvent('controller_initialized')
error_occurred = events.AsyncEvent('error_occurred')
