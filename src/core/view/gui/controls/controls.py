import flet as ft

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
    MESSAGE_SPACING
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
        pass

    def build(self):
        return ft.Container(
            border=BOX_BORDER,
            border_radius=BOX_BORDER_RADIUS,
            padding=BOX_PADDING,
            content=self.build_content()
        )


class NetworkOptionsBox(OptionsBox):
    pass


class HookOptionsBox(OptionsBox):
    def __init__(self):
        super(HookOptionsBox, self).__init__()
        self.hook_picker = ft.FilePicker()
        self.overlay.append(self.hook_picker)

    async def handle_choose_hook_button_click(self, event):
        await self.hook_picker.get_directory_path_async(
            initial_directory='resources/hooks',
            dialog_title=Messages.CHOOSE_HOOK
        )

    def build_content(self):
        return ft.Column(
            controls=[
                ft.Row(
                    controls=[
                        ft.Text(
                            value=Messages.HOOK,
                            size=20,
                            expand=True,
                            text_align=ft.TextAlign.CENTER
                        ),
                    ]
                ),
                ft.Row(
                    controls=[
                        ft.TextField(
                            expand=True,
                            border_color=ft.colors.OUTLINE,
                            read_only=True
                        ),
                        ft.IconButton(
                            icon=ft.icons.FOLDER_OPEN,
                            on_click=self.handle_choose_hook_button_click
                        ),
                    ]
                ),
                ft.Text(
                    'Long long long description',
                    visible=True,
                    max_lines=3,
                    overflow=ft.TextOverflow.ELLIPSIS

                ),
                ft.Container(
                    content=ft.Text(
                        '@author',
                        text_align=ft.TextAlign.RIGHT,
                        italic=True
                    ),
                    alignment=ft.alignment.bottom_right,

                )

            ]
        )


class PayloadOptionsBox(OptionsBox):
    pass


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
    def __init__(self,
                 network_box: CustomControl = network_options_box,
                 hook_box: CustomControl = hook_options_box,
                 payload_box: CustomControl = payload_options_box,
                 process_ctrl_box: CustomControl = process_control_box,
                 msg_box: CustomControl = message_box,
                 message_ctrl_box: CustomControl = message_control_box
                 ):
        self.network_box = network_box
        self.hook_box = hook_box
        self.payload_box = payload_box
        self.process_control_box = process_ctrl_box
        self.message_box = msg_box
        self.message_control_box = message_ctrl_box

    def build(self):
        return ft.Row(
            expand=True,
            controls=[
                ft.Column(
                    expand=True,
                    controls=[
                        self.network_box.build(),
                        self.hook_box.build(),
                        self.payload_box.build(),
                        self.process_control_box.build()
                    ]
                ),
                ft.Column(
                    expand=True,
                    controls=[
                        self.message_box.build(),
                        self.message_control_box.build()
                    ]
                )
            ]
        )
