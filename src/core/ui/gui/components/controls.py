import flet as ft

from src.utils import di
from .base import CustomControl

from .dependencies import (
    network_box_dependency,
    hook_box_dependency,
    payload_box_dependency,
    process_control_box_dependency,
    message_area_box_dependency,
    message_control_box_dependency
)


class MainControl(CustomControl):
    @di.injector.inject
    def build(
            self,
            network=network_box_dependency,
            hook=hook_box_dependency,
            payload=payload_box_dependency,
            process_control=process_control_box_dependency,
            message_area=message_area_box_dependency,
            message_control=message_control_box_dependency
    ):
        return ft.Row(
            expand=True,
            controls=[
                ft.Column(
                    expand=True,
                    controls=[
                        network.build(),
                        hook.build(),
                        payload.build(),
                        process_control.build()
                    ]
                ),
                ft.Column(
                    expand=True,
                    controls=[
                        message_area.build(),
                        message_control.build()
                    ]
                )
            ]
        )
