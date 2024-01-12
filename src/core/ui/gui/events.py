from src.utils import events


class GUIEventChannel(events.EventChannel):
    gui_initialized = events.Event()
    gui_terminated = events.Event()
