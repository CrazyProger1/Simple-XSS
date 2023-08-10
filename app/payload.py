import os
import toml
from settings import (
    PAYLOAD_PACKAGE_FILE,
    PAYLOAD_MAIN_FILE,
    PAYLOAD_INIT_FILE
)
from dataclasses import dataclass
from loguru import logger
from app.exceptions import (
    PayloadLoadingError,
    InitFileImportError
)
from app.utils.helpers import jinja
from app.environment import Environment
from app.utils import imputils


@dataclass
class PayloadMetadata:
    author: str = None
    description: str = None
    version: str = None
    name: str = None


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
        if not isinstance(environment, Environment):
            raise ValueError(f'environment must be type of Environment not {type(environment).__name__}')

        path = str(path)

        if not cls.is_valid(path):
            raise PayloadLoadingError(path)

        main_file = os.path.join(path, PAYLOAD_MAIN_FILE)
        package_file = os.path.join(path, PAYLOAD_PACKAGE_FILE)
        init_file = os.path.join(path, PAYLOAD_INIT_FILE)

        if os.path.isfile(init_file):
            try:
                imputils.import_module_by_filepath(init_file)
            except ImportError:
                raise InitFileImportError(init_file)

        template = jinja.get_template(main_file)

        try:
            package_data = toml.load(package_file)
            metadata = PayloadMetadata(**package_data)
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
