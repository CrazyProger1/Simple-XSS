import flet as ft

from src.utils import di
from ..controls import CustomControl
from src.core.view.gui.controls.dependencies import (
    network_options_box,
    payload_options_box,
    process_control_box,
    message_box,
    message_control_box,
    hook_options_box
)


class MainBox(CustomControl):
    @di.injector.inject
    def build(self, network_box: CustomControl = network_options_box,
              hook_box: CustomControl = hook_options_box,
              payload_box: CustomControl = payload_options_box,
              process_ctrl_box: CustomControl = process_control_box,
              msg_box: CustomControl = message_box,
              message_ctrl_box: CustomControl = message_control_box):
        return ft.Row(
            expand=True,
            controls=[
                ft.Column(
                    expand=True,
                    controls=[
                        network_box.build(),
                        hook_box.build(),
                        payload_box.build(),
                        process_ctrl_box.build()
                    ]
                ),
                ft.Column(
                    expand=True,
                    controls=[
                        msg_box.build(),
                        message_ctrl_box.build()
                    ]
                )
            ]
        )
