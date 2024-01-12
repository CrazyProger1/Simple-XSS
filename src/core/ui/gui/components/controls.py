import asyncio

import flet as ft

from src.utils import di, clsutils
from src.core.context import DefaultContext
from src.core.context.dependencies import current_context_dependency
from src.core.context.events import context_changed

from .base import CustomControl

from .dependencies import (
    network_box_dependency,
    hook_box_dependency,
    payload_box_dependency,
    process_control_box_dependency,
    message_area_box_dependency,
    message_control_box_dependency
)
from ..dependencies import (
    main_page_dependency
)


class MainControl(CustomControl):
    def __init__(self):
        self._setup_controls()
        context_changed.add_listener(self._update_controls)

    @di.injector.inject
    def _setup_controls(self, context: DefaultContext = current_context_dependency):
        for control in clsutils.iter_instances(CustomControl):
            control.setup_data(context=context)

    @di.injector.inject
    def _update_controls(self, context: DefaultContext = current_context_dependency,
                         page: ft.Page = main_page_dependency):
        for control in clsutils.iter_instances(CustomControl):
            control.update_data(context=context)
        asyncio.create_task(page.update_async())

    @di.injector.inject
    def _validate_controls_data(self, context: DefaultContext = current_context_dependency):
        for control in clsutils.iter_instances(CustomControl):
            control.validate_data(context=context)

    @di.injector.inject
    def _save_controls_data(self, context: DefaultContext = current_context_dependency):
        for control in clsutils.iter_instances(CustomControl):
            control.save_data(context=context)

    @di.injector.inject
    def build(
            self,
            network=network_box_dependency,
            hook=hook_box_dependency,
            payload=payload_box_dependency,
            process_control=process_control_box_dependency,
            message_area=message_area_box_dependency,
            message_control=message_control_box_dependency
    ):
        return ft.Row(
            expand=True,
            controls=[
                ft.Column(
                    expand=True,
                    controls=[
                        network.build(),
                        hook.build(),
                        payload.build(),
                        process_control.build()
                    ]
                ),
                ft.Column(
                    expand=True,
                    controls=[
                        message_area.build(),
                        message_control.build()
                    ]
                )
            ]
        )
