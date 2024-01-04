import flet as ft

from src.utils import di

from .components import CustomControl

main_page = di.Dependency(ft.Page)

main_box = di.Dependency(CustomControl)
network_box = di.Dependency(CustomControl)
hook_box = di.Dependency(CustomControl)
payload_box = di.Dependency(CustomControl)
process_control_box = di.Dependency(CustomControl)
message_control_box = di.Dependency(CustomControl)
message_area_box = di.Dependency(CustomControl)
warning_banner = di.Dependency(ft.Banner)
error_banner = di.Dependency(ft.Banner)


def configurate_gui_dependencies():
    from .components import (
        MainBox,
        NetworkBox,
        HookBox,
        PayloadBox,
        MessageAreaBox,
        MessageControlBox,
        ProcessControlBox,
        WarningBanner,
        ErrorBanner
    )

    di.injector.bind(main_box, MainBox())
    di.injector.bind(network_box, NetworkBox())
    di.injector.bind(hook_box, HookBox())
    di.injector.bind(payload_box, PayloadBox())
    di.injector.bind(process_control_box, ProcessControlBox())
    di.injector.bind(message_control_box, MessageControlBox())
    di.injector.bind(message_area_box, MessageAreaBox())
    di.injector.bind(warning_banner, WarningBanner())
    di.injector.bind(error_banner, ErrorBanner())
