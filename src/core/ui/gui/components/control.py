from abc import ABC, abstractmethod


class CustomControl(ABC):
    """Replaces ft.UserControl because of big amount of bugs."""

    overlay = []

    def update_data(self):
        pass

    @abstractmethod
    def build(self): ...
