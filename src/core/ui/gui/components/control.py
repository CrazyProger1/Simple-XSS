from abc import ABC, abstractmethod


class CustomControl(ABC):
    """Replaces ft.UserControl because of big amount of bugs."""

    overlay = []

    def setup_data(self):
        pass

    def update_data(self):
        """Called when the application context changes."""

    def save_data(self):
        """Called when process launched."""

    @abstractmethod
    def build(self): ...
