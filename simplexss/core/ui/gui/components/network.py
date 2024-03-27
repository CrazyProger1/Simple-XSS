import flet as ft

from simplexss.core.transports import BaseTransportServiceFactory
from simplexss.core.tunneling import BaseTunnelingServiceFactory
from simplexss.utils.network import (
    validate_port,
    validate_host,
    validate_url
)
from .enums import Messages
from .constants import (
    TEXT_FONT_SIZE,
    BOX_BORDER,
    BOX_BORDER_RADIUS,
    BOX_PADDING,
)
from ..exceptions import ValidationError
from ..channels import GUIChannel
from ..types import (
    BaseComponent,
)


class NetworkBox(BaseComponent):
    def __init__(
            self,
            tunneling_factory: BaseTunnelingServiceFactory,
            transport_factory: BaseTransportServiceFactory,
    ):
        self._tunneling_factory = tunneling_factory
        self._transport_factory = transport_factory

        self._box_name_text = ft.Text(
            value=Messages.NETWORK,
            size=TEXT_FONT_SIZE,
            expand=True,
            text_align=ft.TextAlign.CENTER
        )
        self._transport_dropdown = ft.Dropdown(
            expand=True,
            border_color=ft.colors.OUTLINE,
            on_change=self._handle_transport_change
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
            on_change=self._handle_host_change
        )

        self._port_field = ft.TextField(
            visible=True,
            width=100,
            border_color=ft.colors.OUTLINE,
            hint_text=Messages.PORT,
            on_change=self._handle_port_change
        )
        self._public_url_field = ft.TextField(
            expand=True,
            border_color=ft.colors.OUTLINE,
            hint_text=Messages.PUBLIC_URL,
            on_change=self._handle_url_change
        )

        self._use_tunneling_checkbox = ft.Checkbox(
            label=Messages.USE_TUNNELLING_SERVICE,
            on_change=self._handle_checkbox_change
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

    async def _handle_checkbox_change(self, e):
        await self.update_async()

    async def _handle_transport_change(self, e):
        self.context.settings.transport.current = self._transport_dropdown.value
        await GUIChannel.need_update.publish_async()

    async def _handle_tunneling_change(self, e):
        self.context.settings.tunneling.current = self._tunneling_dropdown.value
        await GUIChannel.need_update.publish_async()

    async def _handle_host_change(self, e):
        valid = validate_host(self._host_field.value)

        self._host_field.color = ft.colors.RED if not valid else None

        await self._host_field.update_async()

    async def _handle_port_change(self, e):
        port = self._port_field.value

        valid = port.isdigit() and validate_port(int(port))

        self._port_field.color = ft.colors.RED if not valid else None

        await self._port_field.update_async()

    async def _handle_url_change(self, e):
        url = self._public_url_field.value

        valid = validate_url(url)

        self._public_url_field.color = ft.colors.RED if not valid else None

        await self._public_url_field.update_async()

    async def setup_async(self):
        transport = self._transport_factory.get_service(self.context.settings.transport.current)

        self._transport_dropdown.options = [
            ft.dropdown.Option(option)
            for option in self._transport_factory.get_names()
        ]

        if transport is not None:
            self._transport_dropdown.value = transport.NAME

            self._tunneling_dropdown.options = [
                ft.dropdown.Option(option)
                for option in self._tunneling_factory.get_names(transport.PROTOCOL)
            ]

            self._tunneling_dropdown.value = self.context.settings.tunneling.current

        use_tunneling = self.context.settings.tunneling.use
        self._use_tunneling_checkbox.value = use_tunneling
        self._tunneling_dropdown.visible = use_tunneling
        self._public_url_field.visible = not use_tunneling
        self._public_url_field.value = self.context.settings.tunneling.public_url

        self._host_field.value = self.context.settings.transport.host
        self._port_field.value = str(self.context.settings.transport.port)

    async def update_async(self):
        self._container.disabled = self.context.process_running

        use_tunneling = self._use_tunneling_checkbox.value
        self._tunneling_dropdown.visible = use_tunneling
        self._public_url_field.visible = not use_tunneling

        transport = self._transport_factory.get_service(self._transport_dropdown.value)
        if transport is not None:
            self._tunneling_dropdown.options = [
                ft.dropdown.Option(option)
                for option in self._tunneling_factory.get_names(transport.PROTOCOL)
            ]
        await self._container.update_async()

    async def validate_async(self):
        if self._transport_dropdown.value is None:
            raise ValidationError('Please choose transport')

        host = self._host_field.value
        port = self._port_field.value

        if not port.isdigit() or not validate_port(int(port)):
            raise ValidationError('Invalid port')

        if not validate_host(host):
            raise ValidationError('Invalid host')

    async def save_async(self):
        self.context.settings.transport.current = self._transport_dropdown.value
        self.context.settings.transport.port = int(self._port_field.value)
        self.context.settings.transport.host = self._host_field.value
        self.context.settings.tunneling.current = self._tunneling_dropdown.value
        self.context.settings.tunneling.public_url = self._public_url_field.value

    def build(self):
        return self._container
