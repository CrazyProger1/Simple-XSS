import flet as ft

from src.utils import di

from .components import CustomControl

main_page_dependency = di.Dependency(ft.Page)

main_box_dependency = di.Dependency(CustomControl)
network_box_dependency = di.Dependency(CustomControl)
hook_box_dependency = di.Dependency(CustomControl)
payload_box_dependency = di.Dependency(CustomControl)
process_control_box_dependency = di.Dependency(CustomControl)
message_control_box_dependency = di.Dependency(CustomControl)
message_area_box_dependency = di.Dependency(CustomControl)
warning_banner_dependency = di.Dependency(ft.Banner)
error_banner_dependency = di.Dependency(ft.Banner)


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

    di.injector.bind(main_box_dependency, MainBox())
    di.injector.bind(network_box_dependency, NetworkBox())
    di.injector.bind(hook_box_dependency, HookBox())
    di.injector.bind(payload_box_dependency, PayloadBox())
    di.injector.bind(process_control_box_dependency, ProcessControlBox())
    di.injector.bind(message_control_box_dependency, MessageControlBox())
    di.injector.bind(message_area_box_dependency, MessageAreaBox())
    di.injector.bind(warning_banner_dependency, WarningBanner())
    di.injector.bind(error_banner_dependency, ErrorBanner())
