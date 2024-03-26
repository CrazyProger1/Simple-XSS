import flet as ft

from .constants import ICON_SIZE
from .enums import Messages
from ..types import BaseComponent
from ..channels import GUIChannel


class ProcessControlBox(BaseComponent):
    def __init__(self):
        self._launch_button = ft.IconButton(
            icon=ft.icons.PLAY_ARROW,
            icon_size=ICON_SIZE,
            icon_color=ft.colors.GREEN,
            tooltip=Messages.RUN,
            on_click=self._launch_process,
        )

        self._terminate_button = ft.IconButton(
            icon=ft.icons.STOP,
            icon_size=ICON_SIZE,
            icon_color=ft.colors.RED,
            disabled=True,
            tooltip=Messages.STOP,
            on_click=self._terminate_process,
        )
        self._copy_button = ft.IconButton(
            icon=ft.icons.COPY,
            icon_size=ICON_SIZE,
            icon_color=ft.colors.BLUE,
            tooltip=Messages.COPY
        )
        self._hook_field = ft.TextField(
            disabled=True,
            border_color=ft.colors.OUTLINE,
            read_only=True,
            hint_text=Messages.HOOK
        )
        self._container = ft.Row(
            controls=[
                ft.Column(
                    controls=[
                        self._launch_button
                    ]
                ),

                ft.Column(
                    controls=[
                        self._terminate_button
                    ]
                ),
                ft.Column(
                    expand=True,
                    controls=[
                        self._hook_field
                    ]
                ),
                ft.Column(
                    controls=[
                        self._copy_button
                    ]
                ),
            ]
        )

    async def _launch_process(self, e):
        self._terminate_button.disabled = False
        self._launch_button.disabled = True

        await GUIChannel.process_launched.publish_async()

    async def _terminate_process(self, e):
        self._terminate_button.disabled = True
        self._launch_button.disabled = False

        await GUIChannel.process_terminated.publish_async()

    async def update_async(self):
        await self._container.update_async()

    def build(self):
        return self._container
