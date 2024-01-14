from src.utils import di
from .banners import ErrorBanner, WarningBanner
from .types import CustomBanner, CustomControl


class ComponentsDependencyContainer(di.DeclarativeContainer):
    error_banner: CustomBanner = di.Factory(ErrorBanner)
    warning_banner: CustomBanner = di.Factory(WarningBanner)

    main_box: CustomControl
    network_box: CustomControl
    hook_box: CustomControl
    payload_box: CustomControl
    process_box: CustomControl
    message_area_box: CustomControl
    message_sending_box: CustomControl

    @classmethod
    def configure(cls):
        from .controls import (
            MainBox,
            MessageAreaBox,
            MessageSendingBox,
            PayloadBox,
            HookBox,
            NetworkBox,
            ProcessBox
        )

        di.bind(cls.main_box, MainBox())
        di.bind(cls.network_box, NetworkBox())
        di.bind(cls.message_area_box, MessageAreaBox())
        di.bind(cls.message_sending_box, MessageSendingBox())
        di.bind(cls.payload_box, PayloadBox())
        di.bind(cls.hook_box, HookBox())
        di.bind(cls.process_box, ProcessBox())


def configure_components_dependencies():
    ComponentsDependencyContainer.configure()
