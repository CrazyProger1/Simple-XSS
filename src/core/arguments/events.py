from src.utils import events


class ArgumentsEventChannel(events.EventChannel):
    arguments_parsed = events.Event()
