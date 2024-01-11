import flet as ft

from .banner import CustomBanner
from ..enums import Messages
from ..constants import (
    ERROR_BANNER_ICON,
    ERROR_BANNER_ICON_COLOR,
    ERROR_BANNER_TEXT_COLOR,
    ERROR_BANNER_BG_COLOR
)


class ErrorBanner(CustomBanner):
    def __init__(self):
        super(ErrorBanner, self).__init__(
            bgcolor=ERROR_BANNER_BG_COLOR,
            leading=ft.Icon(ERROR_BANNER_ICON, color=ERROR_BANNER_ICON_COLOR, size=40), actions=[
                ft.TextButton(Messages.OK, style=ft.ButtonStyle(color=ERROR_BANNER_TEXT_COLOR), on_click=self.hide),
            ],
        )
