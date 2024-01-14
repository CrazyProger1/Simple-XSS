from src.utils import events


class ContextEventChannel(events.EventChannel):
    context_changed = events.Event()
    context_created = events.Event()
