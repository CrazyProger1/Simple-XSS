from simplexss.core.containers import CoreContainer
from simplexss.utils.di import (
    containers,
    dependencies
)
from .components import (
    MainBox,
    NetworkBox,
    HookBox,
    PayloadBox,
    ProcessControlBox,
    MessageAreaBox,
    MessageControlBox
)
from .banners import (
    ErrorBanner,
    WarningBanner,
)
from .managers import ComponentManager
from .contexts import Context


class GUIContainer(containers.Container):
    main_page = dependencies.Dependency()

    gui_context = dependencies.Factory(
        Context,
        kwargs={
            'settings': CoreContainer.settings,
            'arguments': CoreContainer.arguments
        })

    error_banner = dependencies.Factory(ErrorBanner)
    warning_banner = dependencies.Factory(WarningBanner)

    network_box = dependencies.Factory(NetworkBox, kwargs={
        'tunneling_factory': CoreContainer.tunneling_service_factory,
        'transport_factory': CoreContainer.transport_service_factory,
    })
    hook_box = dependencies.Factory(HookBox, kwargs={
        'manager': CoreContainer.hook_manager,
        'transport_factory': CoreContainer.transport_service_factory,
    })
    payload_box = dependencies.Factory(PayloadBox, kwargs={
        'manager': CoreContainer.payload_manager,
    })
    process_control_box = dependencies.Factory(ProcessControlBox)
    message_area_box = dependencies.Factory(MessageAreaBox, kwargs={
        'io_manager': CoreContainer.io_manager,
    })
    message_control_box = dependencies.Factory(MessageControlBox, kwargs={
        'io_manager': CoreContainer.io_manager,
    })

    main_box = dependencies.Factory(MainBox, kwargs={
        'network_box': network_box,
        'hook_box': hook_box,
        'payload_box': payload_box,
        'process_control_box': process_control_box,
        'message_area_box': message_area_box,
        'message_control_box': message_control_box
    })

    gui_manager = dependencies.Factory(
        ComponentManager,
        kwargs={
            'component': main_box,
            'page': main_page,
            'context': gui_context,
            'error_banner': error_banner,
            'warning_banner': warning_banner,
        }
    )
