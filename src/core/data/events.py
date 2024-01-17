from src.utils import events


class DataEventChannel(events.EventChannel):
    context_changed = events.Event()
