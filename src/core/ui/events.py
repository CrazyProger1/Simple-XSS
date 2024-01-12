from src.utils import events


class UIEventChannel(events.EventChannel):
    ui_initialized = events.Event()
    ui_terminated = events.Event()

    ui_process_activated = events.AsyncEvent()
    ui_process_deactivated = events.AsyncEvent()
