import flet as ft

from src.utils import io

ICON_SIZE = 35
BOX_PADDING = 15
TEXT_FONT_SIZE = 20
DESCRIPTION_MAX_LINES = 3

# Box Border
BOX_BORDER_RADIUS = 5
BOX_BORDER = ft.border.all(1, ft.colors.OUTLINE)

# Messages
MESSAGE_SPACING = 15
MESSAGE_FONT_SIZE = 16
COLOR_TABLE = {
    io.Color.WHITE: ft.colors.WHITE,
    io.Color.RED: ft.colors.RED,
    io.Color.BLUE: ft.colors.BLUE,
    io.Color.YELLOW: ft.colors.YELLOW
}

# Warning banner
WARNING_BANNER_TEXT_COLOR = ft.colors.RED
WARNING_BANNER_ICON_COLOR = ft.colors.AMBER
WARNING_BANNER_BG_COLOR = ft.colors.AMBER_100
WARNING_BANNER_ICON = ft.icons.WARNING_AMBER_ROUNDED

# Error banner
ERROR_BANNER_TEXT_COLOR = ft.colors.RED
ERROR_BANNER_ICON_COLOR = ft.colors.RED
ERROR_BANNER_BG_COLOR = ft.colors.AMBER_100
ERROR_BANNER_ICON = ft.icons.ERROR_ROUNDED
