from src.utils import events


class ApplicationEventChannel(events.EventChannel):
    application_launched = events.Event()
    application_initialized = events.Event()
    application_terminated = events.Event()
