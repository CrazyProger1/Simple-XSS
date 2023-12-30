from src.utils import events

from ..events import interface_initialized

gui_initialized = events.Event('gui_initialized')
gui_initialized.add_listener(interface_initialized)
