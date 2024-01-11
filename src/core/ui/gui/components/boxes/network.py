import asyncio

import flet as ft

from src.utils import di
from src.core.config import (
    DEFAULT_HOST,
    DEFAULT_PORT
)
from src.core.context.dependencies import current_context_dependency
from src.core.transports.dependencies import transport_service_factory_dependency
from src.core.tunneling.dependencies import tunneling_service_factory_dependency
from src.core.ui.utils import validation

from ..base import CustomControl
from src.core.ui.gui.components.constants import (
    TEXT_FONT_SIZE,
    BOX_BORDER,
    BOX_BORDER_RADIUS,
    BOX_PADDING
)
from src.core.ui.gui.components.enums import Messages


class NetworkBox(CustomControl):
    @di.injector.inject
    def __init__(
            self,
            transport_factory=transport_service_factory_dependency,
            tunneling_factory=tunneling_service_factory_dependency
    ):
        super(NetworkBox, self).__init__()
        self._transport_factory = transport_factory
        self._tunneling_factory = tunneling_factory

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
                     transport_factory.get_names()],
            on_change=self._handle_transport_service_change,
            value=None,

        )
        self._host_field = ft.TextField(
            visible=True,
            expand=True,
            border_color=ft.colors.OUTLINE,
            hint_text=Messages.HOST,
            on_change=self._validate_host
        )

        self._port_field = ft.TextField(
            visible=True,
            width=100,
            border_color=ft.colors.OUTLINE,
            hint_text=Messages.PORT,
            on_change=self._validate_port
        )

        self._use_tunneling_service_checkbox = ft.Checkbox(
            on_change=self._handle_tunneling_service_change,
            label=Messages.USE_TUNNELLING_SERVICE
        )
        self._public_url_field = ft.TextField(
            expand=True,
            border_color=ft.colors.OUTLINE,
            hint_text=Messages.PUBLIC_URL,
            on_change=self._validate_url
        )
        self._tunneling_service_dropdown = ft.Dropdown(
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

    async def _handle_transport_service_change(self, event):
        name = self._transport_dropdown.value
        protocol = self._transport_factory.get_protocol(name)

        self._tunneling_service_dropdown.options = [
            ft.dropdown.Option(service) for service in
            self._tunneling_factory.get_names(protocol)
        ]

        await self._tunneling_service_dropdown.update_async()

    async def _handle_tunneling_service_change(self, event: ft.ControlEvent):
        self._use_tunneling_service = event.control.value
        self._public_url_field.visible = not self._use_tunneling_service
        self._tunneling_service_dropdown.visible = self._use_tunneling_service
        await self._public_url_field.update_async()
        await self._tunneling_service_dropdown.update_async()

    def _validate_field(self, field: ft.TextField, *validators):
        if all(validator(field.value) for validator in validators):
            field.color = None
        else:
            field.color = ft.colors.RED

    async def _validate_host(self, event=None):
        self._validate_field(self._host_field, validation.is_valid_host)
        await self._host_field.update_async()

    async def _validate_port(self, event=None):
        self._validate_field(self._port_field, validation.is_valid_port)
        await self._port_field.update_async()

    async def _validate_url(self, event=None):
        self._validate_field(self._public_url_field, validation.is_valid_public_url)
        await self._public_url_field.update_async()

    @di.injector.inject
    def setup_data(self, context=current_context_dependency):
        context = context.unwrap()
        transport_settings = context.settings.transport
        self._transport_dropdown.value = transport_settings.current
        self._host_field.value = transport_settings.host
        self._port_field.value = transport_settings.port

        tunneling_settings = context.settings.tunneling
        use_tunneling_service = tunneling_settings.use
        self._use_tunneling_service_checkbox.value = tunneling_settings.use
        self._tunneling_service_dropdown.value = tunneling_settings.current
        self._public_url_field.value = tunneling_settings.public_url
        self._public_url_field.visible = not use_tunneling_service
        self._tunneling_service_dropdown.visible = use_tunneling_service
        asyncio.create_task(self._content.update_async())

    @di.injector.inject
    def update_data(self, context=current_context_dependency):
        self._content.disabled = context.process_active.unwrap()
        asyncio.create_task(self._content.update_async())

    @di.injector.inject
    def save_data(self, context=current_context_dependency):
        settings = context.settings.unwrap()
        transport = settings.transport
        tunneling = settings.tunneling

        transport.current = self._transport_dropdown.value

        host = self._host_field.value or DEFAULT_HOST
        port = int(self._port_field.value or DEFAULT_PORT)
        if validation.is_valid_host(host=host):
            transport.host = host
        if validation.is_valid_port(port=port):
            transport.port = port

        tunneling.use = self._use_tunneling_service_checkbox.value
        if tunneling.use:
            tunneling.current = self._tunneling_service_dropdown.value
        else:
            url = self._public_url_field.value
            if validation.is_valid_public_url(url=url):
                tunneling.public_url = url

        context.settings = settings

    def build(self):
        return self._content
