import os.path
from abc import ABC, abstractmethod
from functools import cache

import toml
import pathvalidate
from pydantic import BaseModel
from typeguard import typechecked
from loguru import logger

from .enums import Format
from .exceptions import FormatError, FileError


class Loader(ABC):
    format: Format | str = None
    filetypes: set[str] = None

    @classmethod
    @abstractmethod
    def load(cls, schema: type[BaseModel], file: str) -> BaseModel: ...

    @classmethod
    @abstractmethod
    def save(cls, instance: BaseModel, file: str) -> None: ...


class TOMLLoader(Loader):
    format = Format.TOML
    filetypes = {
        '.toml',
    }

    @classmethod
    @typechecked
    def load(cls, schema: type[BaseModel], file: str) -> BaseModel:
        logger.info(f'Loading {schema} from {file}')
        if not os.path.isfile(file):
            raise FileNotFoundError(f'File {file} not found')

        try:
            data = toml.load(file)
        except toml.TomlDecodeError as e:
            logger.error(e)
            raise FormatError(
                fmt=cls.format,
                msg=str(e),
                file=file
            )

        instance = schema.model_validate(data)
        logger.info(f'Loaded {instance}')
        return instance

    @classmethod
    @typechecked
    def save(cls, instance: BaseModel, file: str) -> None:
        logger.info(f'Saving instance of {instance.__class__} to {file}')
        try:
            pathvalidate.validate_filepath(file)
            data = instance.model_dump(warnings=True)
            with open(file, 'w', encoding='utf-8') as f:
                toml.dump(data, f)
            logger.info(f'Saved {instance}')
        except pathvalidate.ValidationError as e:
            logger.error(e)
            raise FileError(
                fmt=cls.format,
                msg=str(e),
                file=file
            )
        except Exception as e:
            logger.error(e)
            raise e


@cache
def get_loader(fmt: Format, file: str, raise_exception: bool = False) -> type[Loader] | None:
    ext = os.path.splitext(file)[1]
    for loader in Loader.__subclasses__():
        if not fmt:
            if isinstance(loader.filetypes, set) and ext in loader.filetypes:
                return loader
        else:
            if loader.format == fmt:
                return loader

    if raise_exception:
        raise ValueError(
            f"Loader can't be detected for file {file} with format {fmt}, "
            f"try specifying valid format or loader directly"
        )
