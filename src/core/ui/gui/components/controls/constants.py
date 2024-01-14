import flet as ft

from src.utils import io

# Box
BOX_BORDER_RADIUS = 5
BOX_BORDER = ft.border.all(1, ft.colors.OUTLINE)
BOX_PADDING = 15

# Text
TEXT_FONT_SIZE = 20
DESCRIPTION_MAX_LINES = 3
INVALID_TEXT_COLOR = ft.colors.RED

# Icons
ICON_SIZE = 35

# Messages
MESSAGE_SPACING = 5
MESSAGE_FONT_SIZE = 15

COLOR_TABLE = {
    io.Color.WHITE: ft.colors.WHITE,
    io.Color.RED: ft.colors.RED,
    io.Color.BLUE: ft.colors.BLUE,
    io.Color.YELLOW: ft.colors.YELLOW
}
