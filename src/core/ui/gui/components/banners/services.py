import flet as ft

from src.utils import di
from ...dependencies import warning_banner, main_page, error_banner
from ...constants import WARNING_BANNER_TEXT_COLOR, ERROR_BANNER_TEXT_COLOR


@di.injector.inject
async def show_warning(text: str, page=main_page, banner=warning_banner):
    banner.page = page
    banner.content = ft.Text(text, color=WARNING_BANNER_TEXT_COLOR)
    await banner.show()


@di.injector.inject
async def show_error(text: str, page=main_page, banner=error_banner):
    banner.page = page
    banner.content = ft.Text(text, color=ERROR_BANNER_TEXT_COLOR)
    await banner.show()
