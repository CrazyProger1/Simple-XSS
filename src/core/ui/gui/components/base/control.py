from abc import ABC, abstractmethod

from src.utils import clsutils
from src.core.context import DefaultContext


class CustomControl(ABC):
    """Replaces ft.UserControl because of big amount of bugs."""

    overlay = []

    def setup_data(self, context: DefaultContext):
        pass

    def update_data(self, context: DefaultContext):
        """Called when the application context changes."""

    def validate_data(self, context: DefaultContext) -> bool:
        """Called before process launched."""

    def save_data(self, context: DefaultContext):
        """Called when process launched."""

    @abstractmethod
    def build(self): ...

