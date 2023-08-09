import os
import toml
from settings import (
    PAYLOAD_DATA_FILE,
    PAYLOAD_MAIN_FILE
)
from dataclasses import dataclass
from app.exceptions import HookLoadingError
from app.utils.helpers import jinja
from app.environment import Environment


@dataclass
class PayloadMetadata:
    author: str = None
    description: str = None
    version: str = None


class Payload:
    @classmethod
    def load(cls, hook_dir: str, environment: Environment) -> "Payload":
        """Loads payload"""
        raise NotImplementedError

    @classmethod
    def is_valid(cls, path: str) -> bool:
        """Determines if payload is valid"""
        raise NotImplementedError

    @property
    def path(self) -> str:
        """Returns payload dir path"""
        raise NotImplementedError

    @property
    def metadata(self) -> PayloadMetadata:
        """Returns payload metadata"""
        raise NotImplementedError

    def __str__(self):
        """Returns payload code"""
        raise NotImplementedError


class DefaultPayload(Payload):
    def __init__(self, code: str, path: str, metadata: PayloadMetadata):
        self._code = code
        self._path = path
        self._metadata = metadata

    @property
    def metadata(self) -> PayloadMetadata:
        return self._metadata

    @classmethod
    def is_valid(cls, path: str) -> bool:
        return os.path.isfile(os.path.join(path, PAYLOAD_MAIN_FILE))

    @classmethod
    def load(cls, path: str, environment: Environment):
        if not cls.is_valid(path):
            raise HookLoadingError(path)

        main_file = os.path.join(path, PAYLOAD_MAIN_FILE)
        data_file = os.path.join(path, PAYLOAD_DATA_FILE)

        template = jinja.get_template(main_file)

        try:
            data = toml.load(data_file)
            metadata = PayloadMetadata(**data)
        except (ValueError, TypeError, toml.TomlDecodeError, FileNotFoundError):
            metadata = PayloadMetadata()

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
