from src.utils import events

interface_initialized = events.AsyncEvent('interface_initialized')
interface_displayed = events.AsyncEvent('interface_displayed')
process_launched = events.AsyncEvent('process_launched')
process_terminated = events.AsyncEvent('process_terminated')
