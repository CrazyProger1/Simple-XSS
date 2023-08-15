import asyncio
import payload
import flet as ft

from time import sleep
from app.exceptions import OptionsLoadingError
from app.hook import DefaultHook
from app.options import Options
from app.payload import DefaultPayload
from app.runner import DefaultRunner
from app.tunneling import HTTPTunnelingAppWrapper
from app.exceptions import ValidationError
from app.validators import validate_url
from settings import (
    APP,
    VERSION,
    OPTIONS_FILE,
    HOOKS_DIR,
    PAYLOADS_DIR
)
from .constants import *
from .io import GUIIOManager


def main(page: ft.Page):
    # To refactor

    page.title = f'{APP} - V{VERSION}'
    page.theme_mode = 'dark'

    message_entered = False
    message_value: str | None = None

    try:
        options = Options.load(OPTIONS_FILE)
    except OptionsLoadingError:
        options = Options()

    runner = DefaultRunner(options=options, io=GUIIOManager())

    def on_print(args: tuple[str]):
        add_message(' '.join(map(str, args)))

    def on_print_pos(args: tuple[str]):
        add_message(' '.join(map(str, args)), color='green')

    def on_print_neg(args: tuple[str]):
        add_message(' '.join(map(str, args)), color='red')

    def on_print_debug(args: tuple[str]):
        add_message(' '.join(map(str, args)), color='blue')

    def on_input(prompt: str):
        nonlocal message_entered

        send_btn.disabled = False
        message_field.disabled = False
        message_field.hint_text = prompt
        page.update()

        while not message_entered:
            sleep(1)

        message_entered = False
        return message_value

    async def on_hook_loaded(hook):
        hook_field.value = hook
        hook_field.disabled = False
        hook_field.update()

    def on_hook_dir_picked(e):
        path = e.path
        load_hook_data(path)

    def on_payload_dir_picked(e):
        path = e.path
        load_payload_data(path)

    def on_checkbox_value_changed(e):
        val = use_tunneling_app_checkbox.value
        tunneling_apps_dropdown.visible = val
        public_url_field.visible = not val

        tunneling_apps_dropdown.update()
        public_url_field.update()

    def on_public_url_field_changed(e):
        val = public_url_field.value

        try:
            validate_url(val)
            public_url_field.color = None
        except ValidationError:
            public_url_field.color = 'red'
        public_url_field.update()

    def run(e):
        run_btn.disabled = True
        stop_btn.disabled = False
        options.use_tunneling_app = use_tunneling_app_checkbox.value
        if options.use_tunneling_app:
            options.tunneling_app = tunneling_apps_dropdown.value
        else:
            options.public_url = public_url_field.value

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

    def add_message(message: str, color: str = None, bg_color: str = None):
        message_box.controls.append(
            ft.Text(
                value=message,
                size=MESSAGE_FONT_SIZE,
                selectable=True,
                color=color,
                bgcolor=bg_color
            )
        )
        page.update()

    def send_message(e):
        nonlocal message_entered, message_value
        message_entered = True
        message_value = message_field.value
        message_field.disabled = True
        message_field.value = None
        add_message(message_value)
        page.update()

    def load_hook_data(path: str):
        if DefaultHook.is_valid(path):
            metadata = DefaultHook.load_metadata(path)

            options.hook_path = path

            hook_box_title.value = 'Hook'
            hook_description_text.value = None
            hook_author_text.value = None

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
        if DefaultPayload.is_valid(path):
            metadata = DefaultPayload.load_metadata(path)

            options.payload_path = path

            payload_box_title.value = 'Payload'
            payload_author_text.value = None
            payload_description_text.value = None

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

    hook_picker = ft.FilePicker(on_result=on_hook_dir_picked)
    payload_picker = ft.FilePicker(on_result=on_payload_dir_picked)

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
        value=options.use_tunneling_app,
        on_change=on_checkbox_value_changed,
        label='Use tunneling app'
    )
    tunneling_apps_dropdown = ft.Dropdown(
        visible=options.use_tunneling_app,
        expand=True,
        border_color=ft.colors.OUTLINE,
        options=list(ft.dropdown.Option(wrapper.app) for wrapper in HTTPTunnelingAppWrapper.__subclasses__()),
        value=options.tunneling_app
    )
    public_url_field = ft.TextField(
        visible=not options.use_tunneling_app,
        expand=True,
        border_color=ft.colors.OUTLINE,
        hint_text='Public URL',
        on_change=on_public_url_field_changed
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
        on_click=send_message
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

    load_payload_data(options.payload_path)
    load_hook_data(options.hook_path)

    public_url_field.value = options.public_url

    DefaultRunner.hook_loaded.add_listener(on_hook_loaded)

    GUIIOManager.input_event.set_listener(on_input)
    GUIIOManager.print_event.add_listener(on_print)
    GUIIOManager.print_pos_event.add_listener(on_print_pos)
    GUIIOManager.print_neg_event.add_listener(on_print_neg)
    GUIIOManager.print_debug_event.add_listener(on_print_debug)

    page.add(main_box)
