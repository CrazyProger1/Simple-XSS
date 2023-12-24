from abc import ABC, abstractmethod
from .hooks import Hook


class HookLoader(ABC):
    @classmethod
    @abstractmethod
    def load(cls, directory: str) -> Hook: ...

    @classmethod
    @abstractmethod
    def save(cls, instance: Hook, directory: str) -> None: ...


class BaseHookLoader(HookLoader):
    @classmethod
    def load(cls, directory: str) -> Hook:
        pass

    @classmethod
    def save(cls, instance: Hook, directory: str) -> None:
        pass
