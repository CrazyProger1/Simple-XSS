import flet as ft

from ..types import BaseComponent


class MainBox(BaseComponent):
    def __init__(
            self,
            network_box: BaseComponent,
            hook_box: BaseComponent,
            payload_box: BaseComponent,
            process_control_box: BaseComponent,
            message_area_box: BaseComponent,
            message_control_box: BaseComponent,
    ):
        self._network_box = network_box
        self._hook_box = hook_box
        self._payload_box = payload_box
        self._process_control_box = process_control_box
        self._message_area_box = message_area_box
        self._message_control_box = message_control_box

    def build(self):
        return ft.Row(
            expand=True,
            controls=[
                ft.Column(
                    expand=True,
                    controls=[
                        self._network_box.build(),
                        self._hook_box.build(),
                        self._payload_box.build(),
                        self._process_control_box.build()
                    ]
                ),
                ft.Column(
                    expand=True,
                    controls=[
                        self._message_area_box.build(),
                        self._message_control_box.build()
                    ]
                )
            ]
        )
