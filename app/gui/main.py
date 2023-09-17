import asyncio
from time import sleep

import flet as ft

from app.hook import DefaultHook
from app.settings import Settings
from app.payload import DefaultPayload
from app.runner import DefaultRunner
from app.tunneling import HTTPTunnelingAppWrapper
from app.utils.settings import Format
from config import (
    APP,
    VERSION,
    SETTINGS_FILE,
    HOOKS_DIR,
    PAYLOADS_DIR
)
from .constants import *
from .io import GUIIOManager


def main(page: ft.Page):
    page.title = f'{APP} - V{VERSION}'
    page.theme_mode = 'dark'
    message_entered = False

    settings = Settings.load(Format.TOML, SETTINGS_FILE)

    runner = DefaultRunner(settings=settings, io=GUIIOManager())

    def on_print(args: tuple[str]):
        add_message(' '.join(map(str, args)))

    def on_input(prompt: str):
        nonlocal message_entered

        send_btn.disabled = False
        message_field.disabled = False
        message_field.hint_text = prompt
        page.update()

        while not message_entered:
            sleep(1)

        message_entered = False
        message = message_field.value
        add_message(message)
        message_field.disabled = True
        message_field.value = None
        page.update()
        return message

    async def on_hook_loaded(hook):
        hook_field.value = hook
        hook_field.disabled = False
        hook_field.update()

    def add_message(message: str):
        message_box.controls.append(
            ft.Text(value=message, size=MESSAGE_FONT_SIZE, selectable=True)
        )
        page.update()

    def run(e):
        run_btn.disabled = True
        stop_btn.disabled = False
        settings.use_tunneling_app = use_tunneling_app_checkbox.value
        if settings.use_tunneling_app:
            settings.tunneling_app = tunneling_apps_dropdown.value
        else:
            settings.public_url = public_url_field.value

        networking_box.disabled = True
        payload_box.disabled = True
        hook_box.disabled = True
        page.update()
        asyncio.run(runner.run())

    def stop(e):
        run_btn.disabled = False
        stop_btn.disabled = True
        networking_box.disabled = False
        payload_box.disabled = False
        hook_box.disabled = False
        hook_field.value = None
        hook_field.disabled = True
        asyncio.run(runner.stop())
        page.update()

    def send(e):
        nonlocal message_entered
        message_entered = True

    def load_hook_data(path: str):
        if path:
            if DefaultHook.is_valid(path):
                metadata = DefaultHook.load_metadata(path)

                settings.hook_path = path

                if metadata.name:
                    hook_box_title.value = str(metadata.name)

                    if metadata.version:
                        hook_box_title.value += f' - V{metadata.version}'

                if metadata.author:
                    hook_author_text.visible = True
                    hook_author_text.value = f'©{metadata.author}'

                hook_path_field.value = path

                if metadata.description:
                    hook_description_text.value = str(metadata.description)
                    hook_description_text.visible = True

                page.update()

    def load_payload_data(path: str):
        if path:
            if DefaultPayload.is_valid(path):
                metadata = DefaultPayload.load_metadata(path)

                settings.payload_path = path

                if metadata.name:
                    payload_box_title.value = str(metadata.name)

                    if metadata.version:
                        payload_box_title.value += f' - V{metadata.version}'

                if metadata.author:
                    payload_author_text.visible = True
                    payload_author_text.value = f'©{metadata.author}'

                payload_path_field.value = path

                if metadata.description:
                    payload_description_text.value = str(metadata.description)
                    payload_description_text.visible = True

                page.update()

    def hook_dir_picked(e):
        path = e.path
        load_hook_data(path)

    def payload_dir_picked(e):
        path = e.path
        load_payload_data(path)

    def checkbox_value_changed(e):
        val = use_tunneling_app_checkbox.value
        tunneling_apps_dropdown.visible = val
        public_url_field.visible = not val

        tunneling_apps_dropdown.update()
        public_url_field.update()

    hook_picker = ft.FilePicker(on_result=hook_dir_picked)
    payload_picker = ft.FilePicker(on_result=payload_dir_picked)

    hook_author_text = ft.Text(
        visible=False,
        text_align=ft.TextAlign.RIGHT,
        italic=True
    )

    hook_author_text_container = ft.Container(
        content=hook_author_text,
        alignment=ft.alignment.bottom_right,
        expand=True
    )

    payload_author_text = ft.Text(
        visible=False,
        text_align=ft.TextAlign.RIGHT,
        italic=True
    )

    payload_author_text_container = ft.Container(
        content=payload_author_text,
        alignment=ft.alignment.bottom_right,
        expand=True
    )

    choose_hook_btn = ft.IconButton(
        icon=ft.icons.FOLDER_OPEN,
        on_click=lambda _: hook_picker.get_directory_path(
            initial_directory=HOOKS_DIR,
            dialog_title='Choose hook'
        )
    )
    hook_path_field = ft.TextField(
        expand=True,
        border_color=ft.colors.OUTLINE,
        read_only=True
    )

    hook_description_text = ft.Text(
        visible=False,
        max_lines=3,
        overflow=ft.TextOverflow.ELLIPSIS

    )

    choose_payload_btn = ft.IconButton(
        icon=ft.icons.FOLDER_OPEN,
        on_click=lambda _: payload_picker.get_directory_path(
            initial_directory=PAYLOADS_DIR,
            dialog_title='Choose payload'
        )

    )
    payload_path_field = ft.TextField(
        expand=True,
        border_color=ft.colors.OUTLINE,
        read_only=True
    )

    payload_description_text = ft.Text(
        visible=False,
        max_lines=3,
        overflow=ft.TextOverflow.ELLIPSIS
    )

    use_tunneling_app_checkbox = ft.Checkbox(
        value=settings.use_tunneling_app,
        on_change=checkbox_value_changed,
        label='Use tunneling app'
    )
    tunneling_apps_dropdown = ft.Dropdown(
        visible=settings.use_tunneling_app,
        expand=True,
        border_color=ft.colors.OUTLINE,
        options=list(ft.dropdown.Option(wrapper.app) for wrapper in HTTPTunnelingAppWrapper.__subclasses__()),
        value=settings.tunneling_app
    )
    public_url_field = ft.TextField(
        visible=not settings.use_tunneling_app,
        expand=True,
        border_color=ft.colors.OUTLINE,
        hint_text='Public URL'
    )
    hook_box_title = ft.Text(
        value='Hook',
        size=TITLE_FONT_SIZE,
        expand=True,
        text_align=ft.TextAlign.CENTER
    )

    payload_box_title = ft.Text(
        value='Payload',
        size=TITLE_FONT_SIZE,
        expand=True,
        text_align=ft.TextAlign.CENTER,
    )

    networking_box_title = ft.Text(
        value='Networking',
        size=TITLE_FONT_SIZE,
        expand=True,
        text_align=ft.TextAlign.CENTER,
    )

    hook_box = ft.Column(
        controls=[
            ft.Row(
                controls=[
                    hook_box_title,
                ]
            ),
            ft.Row(
                controls=[
                    hook_path_field,
                    choose_hook_btn,
                ]
            ),
            hook_description_text,
            hook_author_text_container

        ]
    )

    payload_box = ft.Column(
        expand=True,
        controls=[
            ft.Row(
                controls=[
                    payload_box_title,
                ]
            ),
            ft.Row(
                controls=[
                    payload_path_field,
                    choose_payload_btn,
                ]
            ),

            payload_description_text,
            payload_author_text_container,

        ]
    )

    networking_box = ft.Column(
        expand=True,
        controls=[
            ft.Row(
                controls=[
                    networking_box_title
                ]
            ),
            ft.Row(
                controls=[
                    use_tunneling_app_checkbox
                ]
            ),
            ft.Row(
                controls=[
                    tunneling_apps_dropdown,
                    public_url_field
                ]
            )
        ]
    )
    run_btn = ft.IconButton(
        icon=ft.icons.PLAY_ARROW,
        icon_size=BUTTON_ICON_SIZE,
        icon_color=ft.colors.GREEN,
        on_click=run,
        tooltip='Run'

    )
    stop_btn = ft.IconButton(
        icon=ft.icons.STOP,
        icon_size=BUTTON_ICON_SIZE,
        icon_color=ft.colors.RED,
        disabled=True,
        on_click=stop,
        tooltip='Stop'
    )

    hook_field = ft.TextField(
        disabled=True,
        border_color=ft.colors.OUTLINE,
        read_only=True,
        hint_text='Hook'
    )
    control_box = ft.Row(
        controls=[
            ft.Column(
                controls=[
                    run_btn
                ]
            ),

            ft.Column(
                controls=[
                    stop_btn
                ]
            ),
            ft.Column(
                expand=True,
                controls=[
                    hook_field
                ]
            ),
        ]
    )
    hook_box_container = ft.Container(
        content=hook_box,
        border=ft.border.all(1, ft.colors.OUTLINE),
        border_radius=5,
        padding=CONTAINER_PADDING,
        expand=True,
    )
    payload_box_container = ft.Container(
        content=payload_box,
        border=ft.border.all(1, ft.colors.OUTLINE),
        border_radius=5,
        padding=CONTAINER_PADDING,
        expand=True,
    )
    networking_box_container = ft.Container(
        content=networking_box,
        border=ft.border.all(1, ft.colors.OUTLINE),
        border_radius=5,
        padding=CONTAINER_PADDING,
        expand=True,
    )
    message_field = ft.TextField(
        expand=True,
        border_color=ft.colors.OUTLINE,
        hint_text='Message',
        disabled=True
    )

    send_btn = ft.IconButton(
        icon=ft.icons.SEND,
        icon_size=BUTTON_ICON_SIZE,
        icon_color=ft.colors.BLUE_200,
        tooltip='Send',
        disabled=True,
        on_click=send
    )

    message_box = ft.ListView(
        expand=True,
        spacing=MESSAGE_SPACING,
        auto_scroll=True,
    )
    message_box_container = ft.Container(
        content=message_box,
        border=ft.border.all(1, ft.colors.OUTLINE),
        border_radius=5,
        padding=CONTAINER_PADDING,
        expand=True,
    )

    input_box = ft.Row(
        controls=[
            message_field,
            send_btn
        ]
    )

    left_half_box = ft.Column(
        expand=True,
        controls=[
            hook_box_container,
            payload_box_container,
            networking_box_container,
            control_box
        ]
    )

    right_half_box = ft.Column(
        expand=True,
        controls=[
            message_box_container,
            input_box
        ]
    )

    main_box = ft.Row(
        expand=True,
        controls=[
            left_half_box,
            right_half_box
        ]
    )

    page.overlay.append(hook_picker)
    page.overlay.append(payload_picker)

    load_payload_data(settings.payload_path)
    load_hook_data(settings.hook_path)

    public_url_field.value = settings.public_url

    DefaultRunner.hook_loaded.add_listener(on_hook_loaded)

    GUIIOManager.print_event.add_listener(on_print)
    GUIIOManager.ask_event.set_listener(on_input)

    page.add(main_box)
