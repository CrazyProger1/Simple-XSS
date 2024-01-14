from src.utils import events


class UIEventChannel(events.EventChannel):
    ui_initialized = events.Event()
    ui_terminated = events.Event()

    process_activated = events.AsyncEvent()
    process_deactivated = events.AsyncEvent()
