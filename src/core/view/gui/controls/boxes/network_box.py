import flet as ft

from .options_box import OptionsBox
from ..constants import (
    TEXT_FONT_SIZE,
    BOX_BORDER,
    BOX_BORDER_RADIUS,
    BOX_PADDING
)
from ..enums import Messages


class NetworkOptionsBox(OptionsBox):
    def __init__(self):
        super(NetworkOptionsBox, self).__init__()
        self.use_tunneling_service = False
        self.box_name_text = ft.Text(
            value=Messages.NETWORK,
            size=TEXT_FONT_SIZE,
            expand=True,
            text_align=ft.TextAlign.CENTER
        )
        self.transport_dropdown = ft.Dropdown(
            expand=True,
            border_color=ft.colors.OUTLINE,
            options=[ft.dropdown.Option('http'), ft.dropdown.Option('websocket')],
            value='websocket'
        )
        self.host_field = ft.TextField(
            visible=True,
            expand=True,
            border_color=ft.colors.OUTLINE,
            hint_text=Messages.HOST
        )

        self.port_field = ft.TextField(
            visible=True,
            width=100,
            border_color=ft.colors.OUTLINE,
            hint_text=Messages.PORT
        )

        self.use_tunneling_service_checkbox = ft.Checkbox(
            value=self.use_tunneling_service,
            on_change=self.handle_checkbox_value_change,
            label=Messages.USE_TUNNELLING_SERVICE
        )
        self.public_url_field = ft.TextField(
            visible=not self.use_tunneling_service,
            expand=True,
            border_color=ft.colors.OUTLINE,
            hint_text=Messages.PUBLIC_URL
        )
        self.tunneling_service_dropdown = ft.Dropdown(
            visible=self.use_tunneling_service,
            expand=True,
            border_color=ft.colors.OUTLINE,
            options=[ft.dropdown.Option('ngrok'), ft.dropdown.Option('some app')],
            value='ngrok'
        )

    async def handle_checkbox_value_change(self, event: ft.ControlEvent):
        self.use_tunneling_service = event.control.value
        self.public_url_field.visible = not self.use_tunneling_service
        self.tunneling_service_dropdown.visible = self.use_tunneling_service
        await self.public_url_field.update_async()
        await self.tunneling_service_dropdown.update_async()

    def build(self):
        return ft.Container(
            border=BOX_BORDER,
            border_radius=BOX_BORDER_RADIUS,
            padding=BOX_PADDING,
            content=self.build_content(),
            expand=True
        )

    def build_content(self):
        return ft.Column(
            scroll=ft.ScrollMode.AUTO,
            controls=[
                ft.Row(
                    controls=[
                        self.box_name_text
                    ]
                ),

                ft.Row(
                    controls=[
                        self.transport_dropdown
                    ]
                ),
                ft.Row(
                    controls=[
                        self.host_field,
                        self.port_field
                    ]
                ),
                ft.Divider(),
                ft.Row(
                    controls=[
                        self.use_tunneling_service_checkbox
                    ]
                ),

                ft.Row(
                    controls=[
                        self.tunneling_service_dropdown,
                        self.public_url_field
                    ]
                )

            ]
        )
