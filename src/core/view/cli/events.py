from src.utils import events

from src.core.events import async_mode_entered
from ..events import ui_initialized

cli_initialized = events.AsyncEvent('cli_initialized')
cli_initialized.add_listener(async_mode_entered)
cli_initialized.add_listener(ui_initialized)
