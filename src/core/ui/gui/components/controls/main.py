import flet as ft

from src.utils import di
from ..types import CustomControl
from ..dependencies import ComponentsDependencyContainer


class MainBox(CustomControl):

    @di.inject
    def build(self, network=ComponentsDependencyContainer.network_box,
              hook=ComponentsDependencyContainer.hook_box,
              payload=ComponentsDependencyContainer.payload_box,
              process_control=ComponentsDependencyContainer.process_box,
              message_area=ComponentsDependencyContainer.message_area_box,
              message_control=ComponentsDependencyContainer.message_sending_box):
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
