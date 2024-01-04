import flet as ft

from ..control import CustomControl
from ...constants import ICON_SIZE
from ...enums import Messages


class ProcessControlBox(CustomControl):
    def __init__(self):
        super(ProcessControlBox, self).__init__()
        self._run_button = ft.IconButton(
            icon=ft.icons.PLAY_ARROW,
            icon_size=ICON_SIZE,
            icon_color=ft.colors.GREEN,
            on_click=self._handle_run_button_click,
            tooltip=Messages.RUN
        )
        self._stop_button = ft.IconButton(
            icon=ft.icons.STOP,
            icon_size=ICON_SIZE,
            icon_color=ft.colors.RED,
            disabled=True,
            on_click=self._handle_stop_button_click,
            tooltip=Messages.STOP
        )
        self._copy_button = ft.IconButton(
            icon=ft.icons.COPY,
            icon_size=ICON_SIZE,
            icon_color=ft.colors.BLUE,
            on_click=self._handle_stop_button_click,
            tooltip=Messages.COPY
        )
        self._hook_label = ft.TextField(
            disabled=True,
            border_color=ft.colors.OUTLINE,
            read_only=True,
            hint_text=Messages.HOOK
        )

    async def _handle_run_button_click(self, event):
        pass

    async def _handle_stop_button_click(self, event):
        pass

    def build(self):
        return ft.Row(
            controls=[
                ft.Column(
                    controls=[
                        self._run_button
                    ]
                ),

                ft.Column(
                    controls=[
                        self._stop_button
                    ]
                ),
                ft.Column(
                    expand=True,
                    controls=[
                        self._hook_label
                    ]
                ),
                ft.Column(
                    controls=[
                        self._copy_button
                    ]
                ),
            ]
        )
