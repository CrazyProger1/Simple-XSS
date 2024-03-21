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


class GUIContainer(containers.Container):
    arguments = dependencies.Dependency()
    settings = dependencies.Dependency()

    main_page = dependencies.Dependency()

    network_box = dependencies.Factory(NetworkBox)
    hook_box = dependencies.Factory(HookBox)
    payload_box = dependencies.Factory(PayloadBox)
    process_control_box = dependencies.Factory(ProcessControlBox)
    message_area_box = dependencies.Factory(MessageAreaBox)
    message_control_box = dependencies.Factory(MessageControlBox)

    main_box = dependencies.Factory(MainBox, kwargs={
        'network_box': network_box,
        'hook_box': hook_box,
        'payload_box': payload_box,
        'process_control_box': process_control_box,
        'message_area_box': message_area_box,
        'message_control_box': message_control_box
    })
