import flet as ft

from src.utils import di
from ..dependencies import (
    network_box_dependency,
    hook_box_dependency,
    payload_box_dependency,
    process_control_box_dependency,
    message_area_box_dependency,
    message_control_box_dependency
)
from ..base import CustomControl


class MainBox(CustomControl):
    def __init__(self):
        self._left_part = ft.Column(
            expand=True
        )

        self._right_part = ft.Column(
            expand=True
        )

    @di.injector.inject
    def build(
            self,
            network: CustomControl = network_box_dependency,
            hook: CustomControl = hook_box_dependency,
            payload: CustomControl = payload_box_dependency,
            process_control: CustomControl = process_control_box_dependency,
            message_area: CustomControl = message_area_box_dependency,
            message_control: CustomControl = message_control_box_dependency
    ):
        self._left_part.controls = [
            network.build(),
            hook.build(),
            payload.build(),
            process_control.build()
        ]

        self._right_part.controls = [
            message_area.build(),
            message_control.build()
        ]
        return ft.Row(
            expand=True,
            controls=[
                self._left_part,
                self._right_part
            ]
        )
