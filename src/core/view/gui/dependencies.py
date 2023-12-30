import flet as ft

from src.utils import di
from .controls.custom import CustomControl

current_page = di.Dependency(ft.Page)
main_box = di.Dependency(CustomControl)
payload_options_box = di.Dependency(CustomControl)
hook_options_box = di.Dependency(CustomControl)
network_options_box = di.Dependency(CustomControl)
process_control_box = di.Dependency(CustomControl)
message_box = di.Dependency(CustomControl)
message_control_box = di.Dependency(CustomControl)
