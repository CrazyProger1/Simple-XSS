import flet as ft

from ..constants import ICON_SIZE
from ..custom import CustomControl
from ..enums import Messages


class ProcessControlBox(CustomControl):
    def __init__(self):
        super(ProcessControlBox, self).__init__()
        self.run_button = ft.IconButton(
            icon=ft.icons.PLAY_ARROW,
            icon_size=ICON_SIZE,
            icon_color=ft.colors.GREEN,
            on_click=self.handle_run_button_click,
            tooltip=Messages.RUN
        )
        self.stop_button = ft.IconButton(
            icon=ft.icons.STOP,
            icon_size=ICON_SIZE,
            icon_color=ft.colors.RED,
            disabled=True,
            on_click=self.handle_stop_button_click,
            tooltip=Messages.STOP
        )
        self.copy_button = ft.IconButton(
            icon=ft.icons.COPY,
            icon_size=ICON_SIZE,
            icon_color=ft.colors.BLUE,
            on_click=self.handle_stop_button_click,
            tooltip=Messages.COPY
        )
        self.hook_label = ft.TextField(
            disabled=True,
            border_color=ft.colors.OUTLINE,
            read_only=True,
            hint_text=Messages.HOOK
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
