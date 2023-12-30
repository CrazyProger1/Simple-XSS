import os.path
from abc import ABC, abstractmethod
from functools import cache

import toml
import pathvalidate
from pydantic import BaseModel
from typeguard import typechecked
from loguru import logger

from .enums import Format
from .exceptions import FormatError


class BaseLoader(ABC):
    format: Format | str = None
    filetypes: set[str] = None

    @classmethod
    @abstractmethod
    def load(cls, schema: type[BaseModel], file: str) -> BaseModel: ...

    @classmethod
    @abstractmethod
    def save(cls, instance: BaseModel, file: str) -> None: ...


class TOMLLoader(BaseLoader):
    format = Format.TOML
    filetypes = {
        '.toml',
    }

    @classmethod
    @typechecked
    def load(cls, schema: type[BaseModel], file: str) -> BaseModel:
        """
        Load data from a TOML file and return a validated BaseModel instance.

        Args:
            schema (Type[BaseModel]): The Pydantic model class used for validation.
            file (str): The path to the TOML file containing the data.

        Returns:
            BaseModel: An instance of the validated Pydantic model.

        Raises:
            FileNotFoundError: If the specified file is not found.
            FormatError: If there is an issue with decoding the TOML file.
        """

        logger.debug(f'Loading {schema} from {file}')
        if not os.path.isfile(file):
            logger.error(f'File {file} not found')
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
        logger.debug(f'Loaded {instance}')
        return instance

    @classmethod
    @typechecked
    def save(cls, instance: BaseModel, file: str) -> None:
        """
        Save a BaseModel instance to a TOML file.

        Args:
            instance (BaseModel): The Pydantic model instance to be saved.
            file (str): The path to the TOML file where the data will be saved.

        Raises:
            ValueError: If the file path is invalid.
        """

        logger.debug(f'Saving instance of {instance.__class__} to {file}')
        try:
            pathvalidate.validate_filepath(file)
            data = instance.model_dump(warnings=True)
            with open(file, 'w', encoding='utf-8') as f:
                toml.dump(data, f)
            logger.debug(f'Saved {instance}')
        except pathvalidate.ValidationError as e:
            logger.error(e)
            raise ValueError(f'File path {file} is invalid')
        except Exception as e:
            logger.error(e)
            raise e


@cache
def get_loader(fmt: Format, file: str, raise_exception: bool = False) -> type[BaseLoader] | None:
    """
    Get a data loader class based on the specified format and file extension.

    Args:
        fmt (Format): The desired data format.
        file (str): The path to the file for which the loader is needed.
        raise_exception (bool): Whether to raise an exception if the loader is not found. Default is False.

    Returns:
        Type[BaseLoader] | None: The class of the data loader corresponding to the format, or None if not found.

    Raises:
        ValueError: If the loader cannot be detected for the given file and format, and `raise_exception` is True.
                The exception message includes details about the file and format.

    Note:
        This function caches the result based on the input arguments, providing performance improvement
         for repeated calls with the same arguments.
    """
    ext = os.path.splitext(file)[1]
    for loader in BaseLoader.__subclasses__():
        if not fmt:
            if isinstance(loader.filetypes, set) and ext in loader.filetypes:
                return loader
        else:
            if loader.format == fmt:
                return loader

    if raise_exception:
        logger.error(f"Loader can't be detected for file {file} with format {fmt}")
        raise ValueError(
            f"Loader can't be detected for file {file} with format {fmt}, "
            f"try specifying valid format or loader directly"
        )
