import flet as ft

from simplexss.core.transports import BaseTransportServiceFactory
from simplexss.core.tunneling import BaseTunnelingServiceFactory
from simplexss.core.schemas import (
    ArgumentsSchema,
    SettingsSchema
)
from .enums import Messages
from .constants import (
    TEXT_FONT_SIZE,
    BOX_BORDER,
    BOX_BORDER_RADIUS,
    BOX_PADDING,
)
from ..exceptions import ValidationError
from ..types import BaseComponent


class NetworkBox(BaseComponent):
    def __init__(
            self,
            settings: SettingsSchema,
            arguments: ArgumentsSchema,
            tunneling_factory: BaseTunnelingServiceFactory,
            transport_factory: BaseTransportServiceFactory,

    ):
        self._settings = settings
        self._arguments = arguments
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
        await self.update_async()

    async def setup_async(self):
        transport = self._transport_factory.get_service(self._settings.transport.current)

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

            self._tunneling_dropdown.value = self._settings.tunneling.current

        use_tunneling = self._settings.tunneling.use
        self._use_tunneling_checkbox.value = use_tunneling
        self._tunneling_dropdown.visible = use_tunneling
        self._public_url_field.visible = not use_tunneling
        self._public_url_field.value = self._settings.tunneling.public_url

        self._host_field.value = self._settings.transport.host
        self._port_field.value = self._settings.transport.port

    async def update_async(self):
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
            raise ValidationError('Transport must be selected')

    async def save_async(self):
        pass

    def build(self):
        return self._container
