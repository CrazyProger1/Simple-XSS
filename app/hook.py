import os
import toml
from settings import (
    HOOK_MAIN_FILE,
    HOOK_DATA_FILE
)
from dataclasses import dataclass
from loguru import logger
from app.exceptions import HookLoadingError
from app.utils.helpers import jinja
from app.environment import Environment


@dataclass
class HookMetadata:
    author: str = None
    description: str = None
    version: str = None
    name: str = None


class Hook:
    @classmethod
    def load(cls, path: str, environment: Environment) -> "Hook":
        """Loads hook"""
        raise NotImplementedError

    @classmethod
    def is_valid(cls, path: str) -> bool:
        """Determines if hook is valid"""
        raise NotImplementedError

    @property
    def path(self) -> str:
        """Returns hook dir path"""
        raise NotImplementedError

    @property
    def metadata(self) -> HookMetadata:
        """Returns hook metadata"""
        raise NotImplementedError

    def __str__(self):
        """Returns hook code"""
        raise NotImplementedError


class DefaultHook(Hook):
    def __init__(self, code: str, path: str, metadata: HookMetadata):
        self._code = code
        self._path = path
        self._metadata = metadata

    @property
    def metadata(self) -> HookMetadata:
        return self._metadata

    @classmethod
    def is_valid(cls, path: str) -> bool:
        return os.path.isfile(os.path.join(path, HOOK_MAIN_FILE))

    @classmethod
    def load(cls, path: str, environment: Environment):
        if not cls.is_valid(path):
            raise HookLoadingError(path)

        main_file = os.path.join(path, HOOK_MAIN_FILE)
        data_file = os.path.join(path, HOOK_DATA_FILE)

        template = jinja.get_template(main_file)

        try:
            data = toml.load(data_file)
            metadata = HookMetadata(**data)
        except (ValueError, TypeError, toml.TomlDecodeError, FileNotFoundError):
            metadata = HookMetadata()

        return cls(
            code=template.render(
                environment=environment,
                metadata=metadata
            ),
            path=path,
            metadata=metadata
        )

    @property
    def path(self) -> str:
        return self._path

    def __str__(self):
        return self._code
