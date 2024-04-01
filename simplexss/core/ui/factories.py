from simplexss.utils.clsutils import iter_subclasses
from .types import (
    BaseUI,
    BaseUIFactory
)


class UIFactory(BaseUIFactory):
    def create(self, mode: str) -> BaseUI:
        ui = self.get_ui(mode=mode)
        if ui is None:
            raise ValueError(f'UI not found: {mode}')
        return ui()

    def get_ui(self, mode: str) -> type[BaseUI] | None:
        for ui in iter_subclasses(BaseUI):
            if ui.mode == mode:
                return ui
