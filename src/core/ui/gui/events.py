from src.utils import events


class GUIEventChannel(events.EventChannel):
    gui_initialized = events.Event()
    gui_terminated = events.Event()

    page_initialized = events.Event()

    process_activated = events.AsyncEvent()
    process_deactivated = events.AsyncEvent()

    internal_error_occurred = events.Event(required_kwargs=('error',))
