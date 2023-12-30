from src.core.view.gui.controls.controls import (
    MainBox,
    NetworkOptionsBox,
    PayloadOptionsBox,
    HookOptionsBox,
    ControlBox
)
from .dependencies import (
    main_box,
    payload_options_box,
    hook_options_box,
    network_options_box,
    control_box
)
from src.utils import di


def configurate_dependencies():
    di.injector.bind(control_box, ControlBox())
    di.injector.bind(network_options_box, NetworkOptionsBox())
    di.injector.bind(hook_options_box, HookOptionsBox())
    di.injector.bind(payload_options_box, PayloadOptionsBox())
    di.injector.bind(main_box, MainBox())
