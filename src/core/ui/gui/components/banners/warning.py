import flet as ft

from .banner import CustomBanner
from ...enums import Messages
from ...constants import (
    WARNING_BANNER_ICON_COLOR,
    WARNING_BANNER_ICON,
    WARNING_BANNER_TEXT_COLOR,
    WARNING_BANNER_BG_COLOR
)


class WarningBanner(CustomBanner):
    def __init__(self):
        super(WarningBanner, self).__init__(
            bgcolor=WARNING_BANNER_BG_COLOR,
            leading=ft.Icon(WARNING_BANNER_ICON, color=WARNING_BANNER_ICON_COLOR, size=40), actions=[
                ft.TextButton(Messages.OK, style=ft.ButtonStyle(color=WARNING_BANNER_TEXT_COLOR), on_click=self.hide),
            ],
        )
