import flet as ft

from src.utils import di
from .controls import CustomControl
from .dependencies import current_page, main_box
from .di import configurate_dependencies
from .events import gui_initialized
from .config import (
    WINDOW_SIZE,
    WINDOW_MIN_SIZE,
    THEME
)


@di.injector.inject
def configurate_page(page: ft.Page = current_page):
    page.window_width = WINDOW_SIZE[0]
    page.window_height = WINDOW_SIZE[1]
    page.window_min_width = WINDOW_MIN_SIZE[0]
    page.window_min_height = WINDOW_MIN_SIZE[1]
    page.theme_mode = THEME
    page.overlay.extend(CustomControl.overlay)


@di.injector.inject
async def display(page: ft.Page = current_page, box: CustomControl = main_box):
    await page.add_async(box.build())


def initialize():
    configurate_dependencies()
    configurate_page()


async def launch():
    initialize()
    gui_initialized()
    await display()
