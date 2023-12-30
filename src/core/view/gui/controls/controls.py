import asyncio

import flet as ft

from src.settings.dependencies import current_settings
from src.settings.schemes import DefaultSettingsScheme
from src.utils import di
from .custom import CustomControl
from ..dependencies import (
    network_options_box,
    hook_options_box,
    payload_options_box,
    process_control_box,
    message_box,
    message_control_box
)
from .enums import Messages
from .constants import (
    ICON_SIZE,
    BOX_PADDING,
    BOX_BORDER_RADIUS,
    BOX_BORDER,
    MESSAGE_SPACING,
    TEXT_FONT_SIZE,
    DESCRIPTION_MAX_LINES
)


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


class OptionsBox(CustomControl):
    def build_content(self):
        raise NotImplementedError

    def build(self):
        return ft.Container(
            border=BOX_BORDER,
            border_radius=BOX_BORDER_RADIUS,
            padding=BOX_PADDING,
            content=self.build_content()
        )


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


class HookOptionsBox(OptionsBox):
    def __init__(self):
        super(HookOptionsBox, self).__init__()
        self.hook_picker = ft.FilePicker(on_result=self.handle_hook_chosen)
        self.overlay.append(self.hook_picker)

        self.hook_name_text = ft.Text(
            value=Messages.HOOK,
            size=TEXT_FONT_SIZE,
            expand=True,
            text_align=ft.TextAlign.CENTER
        )
        self.hook_path_field = ft.TextField(
            expand=True,
            border_color=ft.colors.OUTLINE,
            read_only=True
        )
        self.choose_hook_button = ft.IconButton(
            icon=ft.icons.FOLDER_OPEN,
            on_click=self.handle_choose_hook_button_click
        )
        self.hook_description_text = ft.Text(
            visible=True,
            max_lines=DESCRIPTION_MAX_LINES,
            overflow=ft.TextOverflow.ELLIPSIS
        )
        self.hook_author_text = ft.Text(
            text_align=ft.TextAlign.RIGHT,
            italic=True
        )
        self.content = ft.Column(
            controls=[
                ft.Row(
                    controls=[
                        self.hook_name_text
                    ]
                ),
                ft.Row(
                    controls=[
                        self.hook_path_field,
                        self.choose_hook_button,
                    ]
                ),
                self.hook_description_text,
                ft.Container(
                    content=self.hook_author_text,
                    alignment=ft.alignment.bottom_right,

                )

            ]
        )

    def handle_hook_chosen(self, event: ft.FilePickerResultEvent):
        self.hook_path_field.value = event.path
        self.hook_name_text.value = 'Some hook'
        self.hook_description_text.value = 'Some hook desc'
        self.hook_author_text.value = '@author'
        asyncio.create_task(self.content.update_async())

    @di.injector.inject
    async def handle_choose_hook_button_click(self, event, settings: DefaultSettingsScheme = current_settings):
        await self.hook_picker.get_directory_path_async(
            initial_directory=settings.hook.directory,
            dialog_title=Messages.CHOOSE_HOOK_TITLE
        )

    def build_content(self):
        return self.content


class PayloadOptionsBox(OptionsBox):
    def __init__(self):
        super(PayloadOptionsBox, self).__init__()
        self.payload_picker = ft.FilePicker(on_result=self.handle_payload_chosen)
        self.overlay.append(self.payload_picker)

        self.payload_name_text = ft.Text(
            value=Messages.PAYLOAD,
            size=TEXT_FONT_SIZE,
            expand=True,
            text_align=ft.TextAlign.CENTER
        )
        self.payload_path_field = ft.TextField(
            expand=True,
            border_color=ft.colors.OUTLINE,
            read_only=True
        )
        self.choose_payload_button = ft.IconButton(
            icon=ft.icons.FOLDER_OPEN,
            on_click=self.handle_choose_payload_button_click
        )
        self.payload_description_text = ft.Text(
            visible=True,
            max_lines=DESCRIPTION_MAX_LINES,
            overflow=ft.TextOverflow.ELLIPSIS
        )
        self.payload_author_text = ft.Text(
            text_align=ft.TextAlign.RIGHT,
            italic=True
        )
        self.content = ft.Column(
            controls=[
                ft.Row(
                    controls=[
                        self.payload_name_text
                    ]
                ),
                ft.Row(
                    controls=[
                        self.payload_path_field,
                        self.choose_payload_button,
                    ]
                ),
                self.payload_description_text,
                ft.Container(
                    content=self.payload_author_text,
                    alignment=ft.alignment.bottom_right,

                )

            ]
        )

    def handle_payload_chosen(self, event: ft.FilePickerResultEvent):
        self.payload_path_field.value = event.path
        self.payload_name_text.value = 'Some payload'
        self.payload_description_text.value = 'Some payload desc'
        self.payload_author_text.value = '@author'
        asyncio.create_task(self.content.update_async())

    @di.injector.inject
    async def handle_choose_payload_button_click(self, event, settings: DefaultSettingsScheme = current_settings):
        await self.payload_picker.get_directory_path_async(
            initial_directory=settings.payload.directory,
            dialog_title=Messages.CHOOSE_PAYLOAD_TITLE
        )

    def build_content(self):
        return self.content


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


class MainBox(CustomControl):

    @di.injector.inject
    def build(self, network_box: CustomControl = network_options_box,
              hook_box: CustomControl = hook_options_box,
              payload_box: CustomControl = payload_options_box,
              process_ctrl_box: CustomControl = process_control_box,
              msg_box: CustomControl = message_box,
              message_ctrl_box: CustomControl = message_control_box):
        return ft.Row(
            expand=True,
            controls=[
                ft.Column(
                    expand=True,
                    controls=[
                        network_box.build(),
                        hook_box.build(),
                        payload_box.build(),
                        process_ctrl_box.build()
                    ]
                ),
                ft.Column(
                    expand=True,
                    controls=[
                        msg_box.build(),
                        message_ctrl_box.build()
                    ]
                )
            ]
        )
