from src.utils import events

from src.core.events import async_mode_entered
from ..events import ui_initialized


gui_initialized = events.AsyncEvent('gui_initialized')
gui_initialized.add_listener(async_mode_entered)
gui_initialized.add_listener(ui_initialized)
