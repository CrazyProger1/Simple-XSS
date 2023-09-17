import os
import toml
from config import (
    HOOK_MAIN_FILE,
    HOOK_PACKAGE_FILE
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

    @classmethod
    def load_metadata(cls, hook_path: str) -> HookMetadata:
        """Loads hook metadata"""
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
        return path and os.path.isfile(os.path.join(path, HOOK_MAIN_FILE))

    @classmethod
    def load_metadata(cls, hook_path: str) -> HookMetadata:
        package_file = os.path.join(hook_path, HOOK_PACKAGE_FILE)

        try:
            package_data = toml.load(package_file)
            metadata = HookMetadata(**package_data)
        except (ValueError, TypeError, toml.TomlDecodeError, FileNotFoundError):
            metadata = HookMetadata()

        return metadata

    @classmethod
    def load(cls, path: str, environment: Environment):
        if not cls.is_valid(path):
            logger.error(f'Failed to load hook: {path}')
            raise HookLoadingError(path)

        main_file = os.path.join(path, HOOK_MAIN_FILE)

        template = jinja.get_template(main_file)

        metadata = cls.load_metadata(path)

        logger.debug(f'Hook loaded: {path}')
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
