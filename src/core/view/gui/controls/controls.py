import flet as ft

from src.utils import di
from .custom import CustomControl
from ..dependencies import (
    network_options_box,
    hook_options_box,
    payload_options_box,
    control_box
)


class NetworkOptionsBox(CustomControl):
    def build(self):
        return ft.Container(
            border=ft.border.all(1, ft.colors.OUTLINE),
            border_radius=5,
            padding=15,
            # expand=True,
        )


class HookOptionsBox(CustomControl):
    def build(self):
        return ft.Container(
            border=ft.border.all(1, ft.colors.OUTLINE),
            border_radius=5,
            padding=15,
            # expand=True,
        )


class PayloadOptionsBox(CustomControl):
    def build(self):
        return ft.Container(
            border=ft.border.all(1, ft.colors.OUTLINE),
            border_radius=5,
            padding=15,
            # expand=True,
        )


class ControlBox(CustomControl):
    def __init__(self):
        super(ControlBox, self).__init__()
        self.run_button = ft.IconButton(
            icon=ft.icons.PLAY_ARROW,
            icon_size=35,
            icon_color=ft.colors.GREEN,
            on_click=self.handle_run_button_click,
            tooltip='Run'
        )
        self.stop_button = ft.IconButton(
            icon=ft.icons.STOP,
            icon_size=35,
            icon_color=ft.colors.RED,
            disabled=True,
            on_click=self.handle_stop_button_click,
            tooltip='Stop'
        )
        self.copy_button = ft.IconButton(
            icon=ft.icons.COPY,
            icon_size=35,
            icon_color=ft.colors.BLUE,
            on_click=self.handle_stop_button_click,
            tooltip='Copy'
        )
        self.hook_label = ft.TextField(
            disabled=True,
            border_color=ft.colors.OUTLINE,
            read_only=True,
            hint_text='Hook'
        )

    async def handle_run_button_click(self, event):
        pass

    async def handle_stop_button_click(self, event):
        pass

    def build(self):
        return ft.Row(
            controls=[
                ft.Column(
                    controls=[
                        self.run_button
                    ]
                ),

                ft.Column(
                    controls=[
                        self.stop_button
                    ]
                ),
                ft.Column(
                    expand=True,
                    controls=[
                        self.hook_label
                    ]
                ),
                ft.Column(
                    controls=[
                        self.copy_button
                    ]
                ),
            ]
        )


class MainBox(CustomControl):
    @di.injector.inject
    def __init__(self,
                 network_box: CustomControl = network_options_box,
                 hook_box: CustomControl = hook_options_box,
                 payload_box: CustomControl = payload_options_box,
                 control_box: CustomControl = control_box):
        self.network_box = network_box
        self.hook_box = hook_box
        self.payload_box = payload_box
        self.control_box = control_box

    def build(self):
        return ft.Row(
            expand=True,
            controls=[
                ft.Column(
                    expand=True,
                    controls=[
                        self.network_box.build(),
                        self.hook_box.build(),
                        self.payload_box.build(),
                        self.control_box.build()
                    ]
                ),
                ft.Column(
                    expand=True,
                    controls=[

                    ]
                )
            ]
        )
