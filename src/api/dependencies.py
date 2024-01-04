from src.core.dependencies import (
    current_arguments,
    argument_parser,
    plugin_manager,
    plugin_loader,
    settings_scheme
)

from src.core.ui.dependencies import (
    current_ui,
)

from src.core.ui.gui.dependencies import (
    main_page,
    main_box,
    network_box,
    hook_box,
    payload_box,
    process_control_box,
    message_area_box,
    message_control_box
)

__all__ = [
    'current_arguments',
    'argument_parser',
    'plugin_manager',
    'plugin_loader',
    'settings_scheme',
    'current_ui',
    'main_page',
    'main_box',
    'network_box',
    'hook_box',
    'payload_box',
    'process_control_box',
    'message_area_box',
    'message_control_box'
]
