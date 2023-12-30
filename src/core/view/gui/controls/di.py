from .boxes import (
    MessageBox,
    MessageControlBox,
    ProcessControlBox,
    NetworkOptionsBox,
    HookOptionsBox,
    PayloadOptionsBox,
    MainBox
)

from src.core.view.gui.controls.dependencies import (
    main_box,
    payload_options_box,
    hook_options_box,
    network_options_box,
    process_control_box,
    message_box,
    message_control_box
)
from src.utils import di


def configurate_ui_dependencies():
    di.injector.bind(message_box, MessageBox())
    di.injector.bind(message_control_box, MessageControlBox())
    di.injector.bind(process_control_box, ProcessControlBox())
    di.injector.bind(network_options_box, NetworkOptionsBox())
    di.injector.bind(hook_options_box, HookOptionsBox())
    di.injector.bind(payload_options_box, PayloadOptionsBox())
    di.injector.bind(main_box, MainBox())
