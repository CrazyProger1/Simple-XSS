from src.utils import events


class LogicEventChannel(events.EventChannel):
    logic_initialized = events.Event()
    error_occurred = events.Event(required_kwargs=('error',))
