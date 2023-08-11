import flet as ft
from settings import APP, VERSION

MESSAGE_FONT_SIZE = 15
TITLE_FONT_SIZE = 20
BUTTON_ICON_SIZE = 35
CONTAINER_PADDING = 15
MESSAGE_SPACING = 15


def main(page: ft.Page):
    page.title = f'{APP} - V{VERSION}'
    page.theme_mode = 'dark'

    def add_message(message: str):
        message_box.controls.append(
            ft.Text(value=message, size=MESSAGE_FONT_SIZE)
        )
        page.update()

    def run(e):
        run_btn.disabled = True
        stop_btn.disabled = False
        page.update()

    def stop(e):
        run_btn.disabled = False
        stop_btn.disabled = True
        page.update()

    def send(e):
        pass

    def hook_dir_picked(e):
        path = e.path
        if path:
            hook_path_field.value = path
            hook_path_field.update()

            hook_description_text.value = 'Some perfect hook.'
            hook_description_text.visible = True
            hook_description_text.update()

    def payload_dir_picked(e):
        path = e.path
        if path:
            payload_path_field.value = path
            payload_path_field.update()

            payload_description_text.value = 'Some perfect payload.'
            payload_description_text.visible = True
            payload_description_text.update()

    def checkbox_value_changed(e):
        val = use_tunneling_app_checkbox.value
        tunneling_apps_dropdown.visible = val
        public_url_field.visible = not val

        tunneling_apps_dropdown.update()
        public_url_field.update()

    hook_picker = ft.FilePicker(on_result=hook_dir_picked)
    payload_picker = ft.FilePicker(on_result=payload_dir_picked)

    choose_hook_btn = ft.IconButton(
        icon=ft.icons.FOLDER_OPEN,
        on_click=lambda _: hook_picker.get_directory_path()

    )
    hook_path_field = ft.TextField(
        expand=True,
        border_color=ft.colors.OUTLINE,
        read_only=True
    )

    hook_description_text = ft.Text(
        visible=False
    )

    choose_payload_btn = ft.IconButton(
        icon=ft.icons.FOLDER_OPEN,
        on_click=lambda _: payload_picker.get_directory_path()

    )
    payload_path_field = ft.TextField(
        expand=True,
        border_color=ft.colors.OUTLINE,
        read_only=True
    )

    payload_description_text = ft.Text(
        visible=False
    )

    use_tunneling_app_checkbox = ft.Checkbox(
        value=False,
        on_change=checkbox_value_changed,
        label='Use tunneling app'
    )

    tunneling_apps_dropdown = ft.Dropdown(
        visible=False,
        expand=True,
        disabled=False,
        border_color=ft.colors.OUTLINE,
        options=[
            ft.dropdown.Option('ngrok')
        ]
    )
    public_url_field = ft.TextField(
        visible=True,
        expand=True,
        disabled=False,
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
        text_align=ft.TextAlign.CENTER
    )

    networking_box_title = ft.Text(
        value='Networking',
        size=TITLE_FONT_SIZE,
        expand=True,
        text_align=ft.TextAlign.CENTER
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
            ft.Row(
                controls=[
                    hook_description_text
                ]
            )

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
            ft.Row(
                controls=[
                    payload_description_text
                ]
            )

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
    page.add(main_box)

    # file_picker = ft.FilePicker()
    # page.overlay.append(file_picker)
    # page.update()
    #
    # message_box = ft.ListView(
    #     expand=True,
    #     spacing=15,
    #     auto_scroll=True,
    #
    # )
    #
    # hook_box = ft.Column(
    #     expand=True,
    #     controls=[
    #         ft.Row(
    #             controls=[
    #                 ft.Text(
    #                     text_align=ft.TextAlign.CENTER,
    #                     value='Hook',
    #                     expand=True,
    #                     size=20
    #                 ),
    #             ]
    #         ),
    #         ft.Container(
    #             border=ft.border.all(
    #                 1,
    #                 ft.colors.OUTLINE
    #             ),
    #             border_radius=20,
    #             padding=10,
    #             content=ft.Row(
    #                 controls=[
    #                     ft.Text(
    #                         value='C:\\user\\',
    #                         size=18,
    #                         expand=True
    #                     ),
    #                     ft.TextButton(
    #                         "Choose dir...",
    #                         on_click=lambda _: file_picker.pick_files(allow_multiple=False),
    #                         icon=ft.icons.FOLDER_OPEN,
    #
    #                     )
    #                 ]
    #             )
    #         )
    #
    #     ])
    # payload_box = ft.Column(
    #     expand=True,
    #     controls=[
    #         ft.Row(
    #             controls=[
    #                 ft.Text(
    #                     text_align=ft.TextAlign.CENTER,
    #                     value='Payload',
    #                     expand=True,
    #                     size=20
    #                 ),
    #             ]
    #         ),
    #
    #         ft.Container(
    #             border=ft.border.all(
    #                 1,
    #                 ft.colors.OUTLINE
    #             ),
    #             border_radius=20,
    #             padding=10,
    #             content=ft.Row(
    #                 controls=[
    #                     ft.Text(
    #                         value='C:\\user\\',
    #                         size=18,
    #                         expand=True
    #                     ),
    #                     ft.TextButton(
    #                         "Choose dir...",
    #                         on_click=lambda _: file_picker.pick_files(allow_multiple=False),
    #                         icon=ft.icons.FOLDER_OPEN,
    #
    #                     )
    #                 ]
    #             )
    #         )
    #
    #     ])
    # checked = False
    #
    # def on_change(e):
    #     nonlocal checked
    #     checked = not checked
    #     dropdown.disabled = not checked
    #     dropdown.update()
    #
    # dropdown = ft.Dropdown(
    #     expand=True,
    #     disabled=True,
    #     options=[
    #         ft.dropdown.Option("ngrok"),
    #         ft.dropdown.Option("Green"),
    #         ft.dropdown.Option("Blue"),
    #     ]
    # )
    #
    # networking_box = ft.Column(
    #     controls=[
    #         ft.Row(
    #             expand=True,
    #             controls=[
    #                 ft.Text(
    #                     text_align=ft.TextAlign.CENTER,
    #                     value='Networking',
    #                     expand=True,
    #                     size=20
    #                 ),
    #             ]
    #         ),
    #         ft.Row(
    #             expand=True,
    #             controls=[
    #                 dropdown,
    #                 ft.Checkbox(label="Use tunneling app", value=False, on_change=on_change, expand=True)
    #             ]
    #         ),
    #         ft.Row(
    #             expand=True,
    #             controls=[
    #                 ft.TextField(hint_text='Public url', expand=True)
    #             ]
    #         )
    #
    #     ])
    #
    # launch_button = ft.TextButton(
    #     # text='Launch',
    #     expand=True,
    #     height=55,
    #     content=ft.Text(
    #         'Launch',
    #         size=20
    #     )
    # )
    # # stop_button = ft.IconButton(
    # #     icon=ft.icons.SEND_ROUNDED,
    # #     tooltip='Send message',
    # #     scale=1.3
    # # ),
    #
    # stop_button = ft.TextButton(
    #     # text='Launch',
    #     expand=True,
    #     height=55,
    #     disabled=True,
    #     content=ft.Text(
    #         'STOP',
    #         size=20
    #     )
    # )
    #
    # # stop_button = ft.IconButton(
    # #     icon=ft.icons.STOP,
    # #     tooltip='Stop',
    # #     scale=1.3
    # # ),
    #
    # def add_message(message):
    #     message_box.controls.append(
    #         ft.Text(value=message, selectable=True)
    #     )
    #
    # def add_copiable(message):
    #     message_box.controls.append(
    #         ft.Row(
    #             controls=[
    #                 ft.Text(
    #                     value=message
    #                 ),
    #                 ft.IconButton(
    #                     icon=ft.icons.COPY,
    #                     tooltip='Send message',
    #                     scale=0.7,
    #                 )
    #             ]
    #         )
    #         # ft.Text(
    #         #     value=message,
    #         #     selectable=True,
    #         #     italic=True,
    #         #
    #         # ),
    #     )
    #
    # for i in range(100):
    #     add_message(f'msg{i}')
    #
    # add_copiable('test')
    #
    # # launch_button
    #
    # page.add(
    #     ft.Row(
    #         expand=True,
    #         controls=[
    #             ft.Column(
    #                 expand=True,
    #                 controls=[
    #                     ft.Container(
    #                         content=hook_box,
    #                         border=ft.border.all(1, ft.colors.OUTLINE),
    #                         border_radius=5,
    #                         padding=10,
    #                         expand=True,
    #                     ),
    #                     ft.Container(
    #                         content=payload_box,
    #                         border=ft.border.all(1, ft.colors.OUTLINE),
    #                         border_radius=5,
    #                         padding=10,
    #                         expand=True,
    #                     ),
    #                     ft.Container(
    #                         content=networking_box,
    #                         border=ft.border.all(1, ft.colors.OUTLINE),
    #                         border_radius=5,
    #                         padding=10,
    #                         expand=True,
    #                     ),
    #                     ft.Row(
    #                         controls=[
    #                             launch_button,
    #                             stop_button
    #                         ]
    #                     )
    #                 ]
    #             ),
    #             ft.Column(
    #                 expand=True,
    #                 controls=[
    #                     ft.Container(
    #                         content=message_box,
    #                         border=ft.border.all(1, ft.colors.OUTLINE),
    #                         border_radius=5,
    #                         padding=10,
    #                         expand=True,
    #                     ),
    #                     ft.Row(
    #                         controls=[
    #                             ft.TextField(
    #                                 expand=True,
    #                                 hint_text='Message'
    #                             ),
    #                             ft.IconButton(
    #                                 icon=ft.icons.SEND_ROUNDED,
    #                                 tooltip='Send message',
    #                                 scale=1.3
    #                             ),
    #                         ]
    #                     )
    #
    #                 ]
    #             )
    #
    #         ]
    #     ),
    #
    # )
