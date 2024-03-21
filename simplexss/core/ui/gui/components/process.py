import flet as ft

from .constants import ICON_SIZE
from .enums import Messages
from ..types import CustomControl


class ProcessControlBox(CustomControl):
    def __init__(self):
        self._activate_button = ft.IconButton(
            icon=ft.icons.PLAY_ARROW,
            icon_size=ICON_SIZE,
            icon_color=ft.colors.GREEN,
            tooltip=Messages.RUN
        )
        self._deactivate_button = ft.IconButton(
            icon=ft.icons.STOP,
            icon_size=ICON_SIZE,
            icon_color=ft.colors.RED,
            disabled=True,
            tooltip=Messages.STOP
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
                        self._activate_button
                    ]
                ),

                ft.Column(
                    controls=[
                        self._deactivate_button
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

    def build(self):
        return self._container
