from .basic import BannerBasicFunctionality
from .constants import (
    ERROR_BANNER_TEXT_COLOR,
    ERROR_BANNER_BG_COLOR,
    ERROR_BANNER_ICON,
    ERROR_BANNER_ICON_COLOR
)


class ErrorBanner(BannerBasicFunctionality):
    TEXT_COLOR = ERROR_BANNER_TEXT_COLOR
    BG_COLOR = ERROR_BANNER_BG_COLOR
    ICON = ERROR_BANNER_ICON
    ICON_COLOR = ERROR_BANNER_ICON_COLOR
