import os.path
from abc import ABC, abstractmethod

from src.utils import imputils
from src.config import HOOK_FILE, HOOK_CLASS
from .hooks import BaseHook


class BaseHookLoader(ABC):
    @classmethod
    @abstractmethod
    def load(cls, directory: str) -> BaseHook: ...


class HookLoader(BaseHookLoader):
    @classmethod
    def load(cls, directory: str) -> BaseHook:
        hook_file = os.path.join(directory, HOOK_FILE)
        if not os.path.isfile(hook_file):
            raise ValueError(f'File {HOOK_FILE} not found at {directory}')

        hook_class = imputils.import_class_by_filepath(
            hook_file,
            HOOK_CLASS,
            base_class=BaseHook
        )
        hook = hook_class()
        hook.directory = directory
        return hook
