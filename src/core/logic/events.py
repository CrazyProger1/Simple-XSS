from src.utils import events


class LogicEventChannel(events.EventChannel):
    logic_initialized = events.Event()
    logic_terminated = events.Event()
