
import flet as ft

from src.utils import di
from ...dependencies import (
    network_box,
    hook_box,
    payload_box,
    process_control_box,
    message_area_box,
    message_control_box
)
from ..control import CustomControl


class MainBox(CustomControl):
    def __init__(self):
        self._left_part = ft.Column(
            expand=True
        )

        self._right_part = ft.Column(
            expand=True
        )
        self._option_controls = [

        ]

    @di.injector.inject
    def build(
            self,
            network: CustomControl = network_box,
            hook: CustomControl = hook_box,
            payload: CustomControl = payload_box,
            process_control: CustomControl = process_control_box,
            message_area: CustomControl = message_area_box,
            message_control: CustomControl = message_control_box
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
