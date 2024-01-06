import asyncio

import flet as ft

from src.core.dependencies import current_context
from src.core.services import transports, tunneling, context
from src.utils import di
from ..control import CustomControl
from ...constants import (
    TEXT_FONT_SIZE,
    BOX_BORDER,
    BOX_BORDER_RADIUS,
    BOX_PADDING
)
from ...enums import Messages


class NetworkBox(CustomControl):
    def __init__(self):
        super(NetworkBox, self).__init__()
        self._use_tunneling_service = False
        self._box_name_text = ft.Text(
            value=Messages.NETWORK,
            size=TEXT_FONT_SIZE,
            expand=True,
            text_align=ft.TextAlign.CENTER
        )
        self._transport_dropdown = ft.Dropdown(
            expand=True,
            border_color=ft.colors.OUTLINE,
            options=[ft.dropdown.Option(transport) for transport in
                     transports.get_available_transport_service_names()],
            on_change=self._handle_transport_change,
            value=None,

        )
        self._host_field = ft.TextField(
            visible=True,
            expand=True,
            border_color=ft.colors.OUTLINE,
            hint_text=Messages.HOST
        )

        self._port_field = ft.TextField(
            visible=True,
            width=100,
            border_color=ft.colors.OUTLINE,
            hint_text=Messages.PORT
        )

        self._use_tunneling_service_checkbox = ft.Checkbox(
            value=self._use_tunneling_service,
            on_change=self._handle_checkbox_value_change,
            label=Messages.USE_TUNNELLING_SERVICE
        )
        self._public_url_field = ft.TextField(
            visible=not self._use_tunneling_service,
            expand=True,
            border_color=ft.colors.OUTLINE,
            hint_text=Messages.PUBLIC_URL
        )
        self._tunneling_service_dropdown = ft.Dropdown(
            visible=self._use_tunneling_service,
            expand=True,
            border_color=ft.colors.OUTLINE,
        )

        self._content = ft.Container(
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
                            self._use_tunneling_service_checkbox
                        ]
                    ),

                    ft.Row(
                        controls=[
                            self._tunneling_service_dropdown,
                            self._public_url_field
                        ]
                    )

                ]
            ),
            expand=True
        )

    async def _handle_transport_change(self, event):
        name = self._transport_dropdown.value
        protocol = transports.get_transport_protocol(name)

        self._tunneling_service_dropdown.options = [
            ft.dropdown.Option(service) for service in
            tunneling.get_available_tunneling_service_names(protocol)
        ]

        await self._tunneling_service_dropdown.update_async()

    async def _handle_checkbox_value_change(self, event: ft.ControlEvent):
        self._use_tunneling_service = event.control.value
        self._public_url_field.visible = not self._use_tunneling_service
        self._tunneling_service_dropdown.visible = self._use_tunneling_service
        await self._public_url_field.update_async()
        await self._tunneling_service_dropdown.update_async()

    @di.injector.inject
    def update_data(self, appcontext: context.DefaultContext = current_context):
        self._content.disabled = appcontext.active.unwrap()
        asyncio.create_task(self._content.update_async())

    def build(self):
        return self._content
