import flet as ft

from src.utils import di
from src.core.config import (
    DEFAULT_PORT,
    DEFAULT_HOST
)
from src.core.ui.utils import validation
from src.core.data import Context, DataDependencyContainer
from src.core.transports import TransportsDependencyContainer
from src.core.tunneling import TunnelingDependencyContainer

from .utils import show_error
from .constants import (
    BOX_PADDING,
    BOX_BORDER,
    BOX_BORDER_RADIUS,
    TEXT_FONT_SIZE
)
from .utils import validate_field
from ..types import CustomControl
from ...enums import Messages


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
            on_change=self._handle_change_transport
        )

        self._tunneling_dropdown = ft.Dropdown(
            expand=True,
            border_color=ft.colors.OUTLINE,
            on_change=self._handle_change_tunneling
        )
        self._host_field = ft.TextField(
            visible=True,
            expand=True,
            border_color=ft.colors.OUTLINE,
            hint_text=Messages.HOST,
            on_change=self._handle_change_host
        )

        self._port_field = ft.TextField(
            visible=True,
            width=100,
            border_color=ft.colors.OUTLINE,
            hint_text=Messages.PORT,
            on_change=self._handle_change_port
        )
        self._public_url_field = ft.TextField(
            expand=True,
            border_color=ft.colors.OUTLINE,
            hint_text=Messages.PUBLIC_URL,
            on_change=self._handle_change_url
        )

        self._use_tunneling_checkbox = ft.Checkbox(
            label=Messages.USE_TUNNELLING_SERVICE,
            on_change=self._handle_change_checkbox
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

    @di.inject
    def _get_tunneling_options(self,
                               transport_factory=TransportsDependencyContainer.factory,
                               tunneling_factory=TunnelingDependencyContainer.factory,
                               ) -> list[ft.dropdown.Option] | None:
        name = self._transport_dropdown.value
        if name not in transport_factory.get_names():
            return
        protocol = transport_factory.get_transport_protocol(name)
        options = tunneling_factory.get_names(protocol=protocol)
        return [
            ft.dropdown.Option(option)
            for option in options
        ]

    @di.inject
    def _get_transport_options(
            self,
            transport_factory=TransportsDependencyContainer.factory,
    ) -> list[ft.dropdown.Option] | None:
        return [
            ft.dropdown.Option(option)
            for option in transport_factory.get_names()
        ]

    @di.inject
    async def _handle_change_transport(self, _,
                                       context: Context = DataDependencyContainer.context):

        self._tunneling_dropdown.options = self._get_tunneling_options()
        context.settings.transport.current = self._transport_dropdown.value

    @di.inject
    async def _handle_change_tunneling(self, _,
                                       context: Context = DataDependencyContainer.context):
        name = self._tunneling_dropdown.value
        context.settings.tunneling.current = name

    @di.inject
    async def _handle_change_checkbox(self, _,
                                      context: Context = DataDependencyContainer.context):
        use_tunneling = self._use_tunneling_checkbox.value
        self._tunneling_dropdown.visible = use_tunneling
        self._public_url_field.visible = not use_tunneling

        context.settings.tunneling.use = use_tunneling

    async def _handle_change_host(self, _):
        await validate_field(self._host_field, validation.is_valid_host)

    async def _handle_change_port(self, _):
        await validate_field(self._port_field, validation.is_valid_port)

    async def _handle_change_url(self, _):
        await validate_field(self._public_url_field, validation.is_valid_public_url)

    def setup(self, context: Context):
        self._transport_dropdown.options = self._get_transport_options()

        transport_settings = context.settings.transport.unwrap()
        tunneling_settings = context.settings.tunneling.unwrap()
        self._transport_dropdown.value = transport_settings.current
        self._tunneling_dropdown.value = tunneling_settings.current
        self._port_field.value = transport_settings.port
        self._host_field.value = transport_settings.host
        self._public_url_field.value = tunneling_settings.public_url

        self._tunneling_dropdown.options = self._get_tunneling_options()

    def update(self, context: Context):
        self._container.disabled = context.process_active.unwrap()
        use_tunneling = context.settings.tunneling.use.unwrap()
        self._use_tunneling_checkbox.value = use_tunneling
        self._tunneling_dropdown.visible = use_tunneling
        self._public_url_field.visible = not use_tunneling

    def validate(self, context: Context) -> bool:
        host = self._host_field.value
        port = self._port_field.value
        public_url = self._public_url_field.value

        if not validation.is_valid_host(host):
            show_error(Messages.INVALID_HOST_ERROR)
            return False

        if not validation.is_valid_port(port):
            show_error(Messages.INVALID_PORT_ERROR)
            return False

        if not validation.is_valid_public_url(public_url):
            show_error(Messages.INVALID_PUBLIC_URL_ERROR)
            return False
        return True

    def save(self, context: Context):
        host = self._host_field.value or DEFAULT_HOST
        port = self._port_field.value or DEFAULT_PORT
        public_url = self._public_url_field.value

        context.settings.transport.host = host or 'localhost'
        context.settings.transport.port = int(port)
        context.settings.tunneling.public_url = public_url

    def build(self):
        return self._container
