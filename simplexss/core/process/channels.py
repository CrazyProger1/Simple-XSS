from simplexss.utils.events import (
    EventChannel,
    AsyncEvent,
)


class ProcessorChannel(EventChannel):
    error_occurred = AsyncEvent(required_kwargs=('error',))

    process_launched = AsyncEvent()
    process_terminated = AsyncEvent()
