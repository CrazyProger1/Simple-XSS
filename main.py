import flet as ft


class CustomControl:
    """Replaces ft.UserControl because of big amount of bugs."""

    overlay = []

    def build(self):
        raise NotImplementedError


class HookOptionsBox(CustomControl):
    def __init__(self):
        super(HookOptionsBox, self).__init__()
        self.hook_picker = ft.FilePicker(on_result=self.handle_hook_dir_pick)
        self.overlay.append(self.hook_picker)

    async def handle_hook_dir_pick(self, event):
        pass

    async def handle_choose_hook_button_click(self, event):
        await self.hook_picker.get_directory_path_async(
            initial_directory='resources/hooks',
            dialog_title='Choose hook'
        )

    def build(self):
        return ft.Container(
            content=ft.Column(
                controls=[
                    ft.Row(
                        controls=[
                            ft.Text(
                                value='Hook',
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
            ),
            border=ft.border.all(1, ft.colors.OUTLINE),
            border_radius=5,
            padding=15,
            # expand=True,
        )


class PayloadOptionsBox(CustomControl):
    def build(self):
        return ft.Container(
            content=ft.Column(
                controls=[
                    ft.Row(
                        controls=[
                            ft.Text(
                                value='Payload',
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
            ),
            border=ft.border.all(1, ft.colors.OUTLINE),
            border_radius=5,
            padding=15,

            # expand=True,
        )


class NetworkOptionsBox(CustomControl):
    def __init__(self):
        super(NetworkOptionsBox, self).__init__()
        self.value = False

    async def handle_checkbox_value_change(self, event):
        self.value = not self.value

    def build(self):
        return ft.Container(
            content=ft.Column(
                controls=[
                    ft.Row(
                        controls=[
                            ft.Text(
                                value='Network',
                                size=20,
                                expand=True,
                                text_align=ft.TextAlign.CENTER
                            ),
                        ]
                    ),
                    ft.Row(
                        controls=[
                            ft.Dropdown(
                                expand=True,
                                border_color=ft.colors.OUTLINE,
                                options=[ft.dropdown.Option('http'), ft.dropdown.Option('websocket')],
                                value='websocket'
                            )

                        ]
                    ),
                    ft.Row(
                        controls=[
                            ft.Checkbox(
                                value=self.value,
                                on_change=self.handle_checkbox_value_change,
                                label='Use tunneling service'
                            ),

                        ]
                    ),

                    ft.Row(
                        controls=[
                            ft.Dropdown(
                                visible=self.value,
                                expand=True,
                                border_color=ft.colors.OUTLINE,
                                options=[ft.dropdown.Option('ngrok'), ft.dropdown.Option('some app')],
                                value='ngrok'
                            ),
                            ft.TextField(
                                visible=not self.value,
                                expand=True,
                                border_color=ft.colors.OUTLINE,
                                hint_text='Public URL'
                            )
                        ]
                    )

                ]
            ),
            border=ft.border.all(1, ft.colors.OUTLINE),
            border_radius=5,
            padding=15,
            expand=True,
        )


class ControlBox(CustomControl):
    def __init__(self):
        super(ControlBox, self).__init__()
        self.run_button = ft.IconButton(
            icon=ft.icons.PLAY_ARROW,
            icon_size=35,
            icon_color=ft.colors.GREEN,
            on_click=self.handle_run_button_click,
            tooltip='Run'
        )
        self.stop_button = ft.IconButton(
            icon=ft.icons.STOP,
            icon_size=35,
            icon_color=ft.colors.RED,
            disabled=True,
            on_click=self.handle_stop_button_click,
            tooltip='Stop'
        )
        self.copy_button = ft.IconButton(
            icon=ft.icons.COPY,
            icon_size=35,
            icon_color=ft.colors.BLUE,
            on_click=self.handle_stop_button_click,
            tooltip='Copy'
        )
        self.hook_label = ft.TextField(
            disabled=True,
            border_color=ft.colors.OUTLINE,
            read_only=True,
            hint_text='Hook'
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


class MessageBox(CustomControl):
    def build(self):
        return ft.Row(
            expand=True,
            controls=[
                ft.Container(
                    content=ft.ListView(
                        expand=True,
                        spacing=15,
                        auto_scroll=True,
                    ),
                    border=ft.border.all(1, ft.colors.OUTLINE),
                    border_radius=5,
                    padding=15,
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
                    hint_text='Message',
                    disabled=True
                ),
                ft.IconButton(
                    icon=ft.icons.SEND,
                    icon_size=35,
                    icon_color=ft.colors.BLUE_200,
                    tooltip='Send',
                    disabled=True,
                    on_click=self.handle_send_button_click
                )

            ]
        )


class MainBox(CustomControl):
    def __init__(self):
        super(MainBox, self).__init__()
        self.hook_box = HookOptionsBox()
        self.payload_box = PayloadOptionsBox()
        self.network_box = NetworkOptionsBox()
        self.control_box = ControlBox()
        self.message_box = MessageBox()
        self.message_control_box = MessageControlBox()

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
                        self.control_box.build()
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


async def main(page: ft.Page):
    page.window_width = 1280
    page.window_height = 760
    page.window_min_width = 1280
    page.window_min_height = 760

    page.theme_mode = 'dark'
    main_box = MainBox()
    page.overlay.extend(CustomControl.overlay)
    await page.add_async(main_box.build())


ft.app(target=main)
