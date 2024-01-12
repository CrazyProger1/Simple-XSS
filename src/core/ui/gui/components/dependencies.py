import flet as ft

from src.utils import di

from .base import CustomControl

main_control_dependency = di.Dependency(CustomControl)
network_box_dependency = di.Dependency(CustomControl)
hook_box_dependency = di.Dependency(CustomControl)
payload_box_dependency = di.Dependency(CustomControl)
process_control_box_dependency = di.Dependency(CustomControl)
message_control_box_dependency = di.Dependency(CustomControl)
message_area_box_dependency = di.Dependency(CustomControl)
warning_banner_dependency = di.Dependency(ft.Banner)
error_banner_dependency = di.Dependency(ft.Banner)


def configurate_components_dependencies():
    from .boxes import (
        NetworkBox,
        HookBox,
        PayloadBox,
        ProcessControlBox,
        MessageAreaBox,
        MessageControlBox,
    )
    from .banners import (
        WarningBanner,
        ErrorBanner
    )
    from .controls import MainControl

    di.injector.bind(network_box_dependency, NetworkBox())
    di.injector.bind(hook_box_dependency, HookBox())
    di.injector.bind(payload_box_dependency, PayloadBox())
    di.injector.bind(process_control_box_dependency, ProcessControlBox())
    di.injector.bind(message_control_box_dependency, MessageControlBox())
    di.injector.bind(message_area_box_dependency, MessageAreaBox())
    di.injector.bind(warning_banner_dependency, WarningBanner())
    di.injector.bind(error_banner_dependency, ErrorBanner())
    di.injector.bind(main_control_dependency, MainControl())
