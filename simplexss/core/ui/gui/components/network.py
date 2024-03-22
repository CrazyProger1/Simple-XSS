import flet as ft

from simplexss.core.enums import Transport
from .enums import Messages
from .constants import (
    TEXT_FONT_SIZE,
    BOX_BORDER,
    BOX_BORDER_RADIUS,
    BOX_PADDING,
)
from ..types import CustomControl


class NetworkBox(CustomControl):
    def __init__(self):
        self._box_name_text = ft.Text(
            value=Messages.NETWORK,
            size=TEXT_FONT_SIZE,
            expand=True,
            text_align=ft.TextAlign.CENTER
        )
        self._transport_dropdown = ft.Dropdown(
            expand=True,
            border_color=ft.colors.OUTLINE,
            options=[
                ft.dropdown.Option(transport.value)
                for transport in Transport
            ]
        )

        self._tunneling_dropdown = ft.Dropdown(
            expand=True,
            border_color=ft.colors.OUTLINE,
        )
        self._host_field = ft.TextField(
            visible=True,
            expand=True,
            border_color=ft.colors.OUTLINE,
            hint_text=Messages.HOST,
        )

        self._port_field = ft.TextField(
            visible=True,
            width=100,
            border_color=ft.colors.OUTLINE,
            hint_text=Messages.PORT,
        )
        self._public_url_field = ft.TextField(
            expand=True,
            border_color=ft.colors.OUTLINE,
            hint_text=Messages.PUBLIC_URL,
        )

        self._use_tunneling_checkbox = ft.Checkbox(
            label=Messages.USE_TUNNELLING_SERVICE,
        )

        self._container = ft.Container(
            border=BOX_BORDER,
            border_radius=BOX_BORDER_RADIUS,
            padding=BOX_PADDING,
            content=ft.Column(
                scroll=ft.ScrollMode.AUTO,
                controls=[
                    ft.Row(
                        controls=[
                            self._box_name_text
                        ]
                    ),

                    ft.Row(
                        controls=[
                            self._transport_dropdown
                        ]
                    ),
                    ft.Row(
                        controls=[
                            self._host_field,
                            self._port_field
                        ]
                    ),
                    ft.Divider(),
                    ft.Row(
                        controls=[
                            self._use_tunneling_checkbox
                        ]
                    ),

                    ft.Row(
                        controls=[
                            self._tunneling_dropdown,
                            self._public_url_field
                        ]
                    )

                ]
            ),
            expand=True
        )

    def build(self):
        return self._container
