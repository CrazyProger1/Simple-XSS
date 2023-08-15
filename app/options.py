import os
import toml
from dataclasses import dataclass
from settings import (
    DEFAULT_HOOK,
    DEFAULT_PAYLOAD,
    DEFAULT_TUNNELING_APP,
    DEFAULT_HOST,
    DEFAULT_PORT,
    OPTIONS_FILE,
    USE_TUNNELING_APP
)

from loguru import logger
from app.exceptions import OptionsLoadingError, OptionsSavingError


@dataclass
class Options:
    """"""
    public_url: str = None
    payload_path: str = DEFAULT_PAYLOAD
    hook_path: str = DEFAULT_HOOK
    use_tunneling_app: bool = USE_TUNNELING_APP
    tunneling_app: str = DEFAULT_TUNNELING_APP
    host: str = DEFAULT_HOST
    port: int = DEFAULT_PORT

    @classmethod
    def load(cls, path: str = OPTIONS_FILE):
        if os.path.isfile(path):
            try:
                options_data = toml.load(path)
            except (ValueError, TypeError, toml.TomlDecodeError):
                logger.error(f'Failed to load options: {path}')
                raise OptionsLoadingError(path)

            try:
                logger.debug(f'Options loaded: {options_data}')
                return cls(**options_data)
            except TypeError:
                return cls()
        else:
            logger.error(f'Failed to load options: {path}')
            raise OptionsLoadingError(path)

    def save(self, path: str = OPTIONS_FILE):
        try:
            with open(path, 'w') as of:
                toml.dump(self.__dict__, of)
        except Exception as e:
            raise OptionsSavingError(path)
