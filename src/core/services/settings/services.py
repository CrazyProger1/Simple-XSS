from pydantic import BaseModel

from src.utils import settings as setutil

from src.core.config import DEFAULT_SETTINGS_FILE


def load_settings(
        scheme: type[BaseModel],
        file: str):
    try:
        settings = setutil.load(schema=scheme, file=file)
    except (FileNotFoundError, setutil.exceptions.FormatError, ValueError):
        settings = scheme()
        setutil.save(instance=settings, file=file)

    return settings


def save_settings(
        settings: BaseModel,
        file: str):
    try:
        setutil.save(instance=settings, file=file)
    except ValueError:
        setutil.save(instance=settings, file=DEFAULT_SETTINGS_FILE)
