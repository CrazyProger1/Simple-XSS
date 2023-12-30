import flet as ft

from src.core.view.gui.controls.constants import (
    MESSAGE_SPACING,
    BOX_BORDER,
    BOX_BORDER_RADIUS,
    BOX_PADDING,
    ICON_SIZE
)
from ..custom import CustomControl
from ..enums import Messages


class MessageBox(CustomControl):
    def build(self):
        return ft.Row(
            expand=True,
            controls=[
                ft.Container(
                    content=ft.ListView(
                        expand=True,
                        spacing=MESSAGE_SPACING,
                        auto_scroll=True,
                    ),
                    border=BOX_BORDER,
                    border_radius=BOX_BORDER_RADIUS,
                    padding=BOX_PADDING,
                    expand=True,
                )
            ]

        )


class MessageControlBox(CustomControl):
    async def handle_send_button_click(self, event):
        pass

    def build(self):
        return ft.Row(
            controls=[
                ft.TextField(
                    expand=True,
                    border_color=ft.colors.OUTLINE,
                    hint_text=Messages.MESSAGE,
                    disabled=True
                ),
                ft.IconButton(
                    icon=ft.icons.SEND,
                    icon_size=ICON_SIZE,
                    icon_color=ft.colors.BLUE_200,
                    tooltip=Messages.SEND,
                    disabled=True,
                    on_click=self.handle_send_button_click
                )

            ]
        )
